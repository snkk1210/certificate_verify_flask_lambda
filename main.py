#!/bin/python3

from flask import Flask, render_template
import flask
import subprocess
import os
import glob
app = Flask(__name__)

@app.route('/')
def lambda_handler(event=None, context=None):
	return render_template('layout.html')

@app.route('/certificate-upload', methods=['POST'])
def crtupload():
    if 'certificate' not in flask.request.files:
        return render_template('layout.html', message="ファイル未指定です")
    # ファイルの保存
    fs = flask.request.files['certificate']
    fs.save('/tmp/certificate.crt')
    
    # 証明書が空であるか判定
    crtsize = os.path.getsize('/tmp/certificate.crt')
    if crtsize == 0:
      return render_template('layout.html', message="＊証明書を選択してアップロードしてください")
    else:
      return render_template('layout.html', message="＊証明書のアップロードが完了しました")

@app.route('/privatekey-upload', methods=['POST'])
def keyupload():
    if 'privatekey' not in flask.request.files:
        return render_template('layout.html', message="ファイル未指定です")
    # ファイルの保存
    fs = flask.request.files['privatekey']
    fs.save('/tmp/privatekey.key')
    
    # 秘密鍵が空であるか判定
    keysize = os.path.getsize('/tmp/privatekey.key')
    if keysize == 0:
      return render_template('layout.html', message="＊秘密鍵を選択してアップロードしてください")
    else:
      return render_template('layout.html', message="＊秘密鍵のアップロードが完了しました")

@app.route('/ca-upload', methods=['POST'])
def caupload():
    if 'intermediate' not in flask.request.files:
        return render_template('layout.html', message="ファイル未指定です")
    # ファイルの保存
    fs = flask.request.files['intermediate']
    fs.save('/tmp/intermediate.ca')

    # 中間証明書が空であるか判定
    casize = os.path.getsize('/tmp/intermediate.ca')
    if casize == 0:
      return render_template('layout.html', message="＊中間証明書を選択してアップロードしてください")
    else:
      return render_template('layout.html', message="＊中間証明書のアップロードが完了しました")

@app.route('/exec-script', methods=['POST'])
def exec():
  
	certificate_fs = flask.request.files['certificate']
	certificate_fs.save('./certificate.crt')
	privatekey_fs = flask.request.files['privatekey']
	privatekey_fs.save('./privatekey.key')
	intermediate_fs = flask.request.files['intermediate']
	intermediate_fs.save('./intermediate.ca')

	res = subprocess.run('./app/cert_check.sh ./certificate.crt ./privatekey.key ./intermediate.ca', shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	# 一時ファイルを削除
	#for tmpfile in glob.glob('./*'):
	#	os.remove(tmpfile)
	#for crtfile in glob.glob('./*'):
	#	os.remove(crtfile)

	#return res.stdout.decode("utf8")
	mes = res.stdout.decode("utf8")
	return render_template('layout.html', result=mes, restitle="実行結果")

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
