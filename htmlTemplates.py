css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    transition: background-color 0.3s ease;
}
.chat-message:hover {
    background-color: lighten(#475063, 5%);
}
.chat-message.user {
    background-color: #2b313e; /* Darker shade for user */
    align-items: self-end; /* Aligns user messages to the right */
}
.chat-message.bot {
    background-color: #475063; /* Lighter shade for bot */
    align-items: self-start; /* Aligns bot messages to the left */
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff; /* Ensures text is white */
    font-size: 1rem; /* Adjust font size */
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
