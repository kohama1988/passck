import requests, json
from flask import Flask,render_template
from threading import Timer

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Cookie': 'Hm_lvt_b957667300eff41ee03e59e191c81545=1615039455; Hm_lpvt_b957667300eff41ee03e59e191c81545=1615627474; JSESSIONID=1bd0zzbz2karehfxy66yktty5; pcxSessionId=05b0b2ff-a4e5-4ac8-8c64-dff5f673e50a; tgw_l7_route=a7675a6831a3996a7f1b08f285478767',
}

data = {'addressName': ''}
url = 'https://ppt.mfa.gov.cn/appo/service/reservation/data/getReservationDateBean.json?rid=0.7495038520701878'

@app.route('/')
def index():
    check_update()
    return render_template('index.html')

# @app.route('/check_update/')
def check_update():
    date = []
    web = requests.post(url, headers=headers, data=data)
    info = json.loads(web.text)

    for i in info['data']:
        date.append(i['date'])
    target = ['2021-04-05', '2021-04-06', '2021-04-07', '2021-04-08', '2021-04-09']
    for i in target:
        if i in date:
            send_notify('領事館ページにパスポート更新情報がありました！')


def send_notify(notification_message):
    line_notify_token = ''
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': notification_message}
    requests.post(line_notify_api, headers = headers, data = data)

# send_notify('領事館ページにパスポート更新情報がありました！')

if __name__ == '__main__':
    app.run()

