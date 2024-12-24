from flask import Blueprint, render_template, request, jsonify, redirect,url_for,session
from app.utils.voice_recognition import recognize_file
from app.utils.chat_assistant import chat
from app.utils.database import insert_user, insert_message, get_conversation, get_userid

routes = Blueprint('routes',__name__)


@routes.route('/chats', methods=['POST'])
def chats():

    # 訊息部分
    try:
        data = request.json

        if 'message' not in data:
            return jsonify({'error':'No message provided'}), 400

        user_message = data['message']
    
    # 音訊部分
    except:
        if 'audio' not in request.files:
            return jsonify({'error':'No audio file found'}), 400
        
        audio_file = request.files['audio']

        try:
            # Process the audio file for speech recognition
            user_message = recognize_file(audio_file)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    # model的回應
    reply = chat(new_content=user_message)
    # reply = user_message

    # 加到資料庫
    insert_message(user_id=session['userid'],role='user',message=user_message)
    insert_message(user_id=session['userid'],role='assistant',message=reply)

    return jsonify({'user_message':user_message,'reply':reply})

    
@routes.route('/', methods = ['POST','GET'])
def home():

    if request.method == 'POST':
        username = request.form['username']

        # 確認是否有該使用者存在
        userid = get_userid(username=username)

        if userid is None:
            userid = insert_user(username=username)

        session['username'] = username    
        session['userid'] = userid
        return redirect(url_for('routes.chat_page'))
        
    return render_template('home.html')

@routes.route('/chat_page')
def chat_page():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('routes.home'))
    
    # Retrieve the conversation from the session
    conversation = get_conversation(username=username)
    # print(conversation)
    
    return render_template('chat_page.html', username=username,conversation=conversation)