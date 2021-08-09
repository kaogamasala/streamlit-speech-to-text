import os

from google.cloud import speech
from google.cloud import storage as gcs
#import io

import streamlit as st

#環境変数
#ローカル
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Key/service_account.json'

bucket_name = "speechtotext20210801"
fname = "service_account.json"
project_name = "Speech-to-text-20210801

client = gcs.Client(project_name)
bucket = client.get_bucket(bucket_name)
blob = gcs.Blob(fname, bucket)
service_account = blob.download_as_string()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account


# speech-to-text
def transcribe_file(content, lang='日本語'):
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP',
        'スペイン語': 'es-ES'
    }
    client = speech.SpeechClient()
    #streamlitではない場合に使用
    #with io.open(speech_file, 'rb') as f:
    #   content = f.read()

    audio = speech.RecognitionAudio(content = content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    #    sample_rate_hertz=16000,
        language_code = lang_code[lang]
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        st.write(result.alternatives[0].transcript)

        #print(result)
        #print("認識結果: {}".format(result.alternatives[0].transcript))

st.title('文字起こしアプリ')
st.header('概要')
st.markdown('<a href="https://cloud.google.com/speech-to-text?hl=ja">Google Cloud Speech-to-textを使用した文字起こしアプリです。</a>', unsafe_allow_html=True)

upload_file = st.file_uploader('ファイルのアップロード', type=['mp3', 'wav'])
if upload_file is not None:
    content = upload_file.read()
    st.subheader('ファイル詳細')
    file_details = {'FileName': upload_file.name, 'FileType': upload_file.type, 'FileSize': upload_file.size}
    st.write(file_details)
    st.subheader('音声の再生')
    st.audio(content)

    st.subheader('言語選択')
    option = st.selectbox('翻訳言語を選択してください',
                         ('英語', '日本語', 'スペイン語') )
    st.write('選択中の言語:', option)                     

    st.write('文字起こし')
    if st.button('開始'):
        comment = st.empty()
        comment.write('文字起こしを開始します')
        transcribe_file(content, lang=option)
        comment.write('完了しました')