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

@app.route('/exec', methods=['POST'])
def exec():
  
	cert_fs = flask.request.files['cert']
	cert_fs.save('/tmp/cert.pem')
	privkey_fs = flask.request.files['privkey']
	privkey_fs.save('/tmp/privkey.pem')
	chain_fs = flask.request.files['chain']
	chain_fs.save('/tmp/chain.pem')

	res = subprocess.run('./app/cert_check.sh /tmp/cert.pem /tmp/privkey.pem /tmp/chain.pem', shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	# 一時ファイルを削除
	for tmpfile in glob.glob('/tmp/*.pem'):
		os.remove(tmpfile)

	mes = res.stdout.decode("utf8")
	return render_template('layout.html', result=mes, restitle="実行結果")

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
