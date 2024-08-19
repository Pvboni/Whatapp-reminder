import pywhatkit as kit

def enviar_mensagem():
    # Substitua 'SEU_NUMERO' pelo número de telefone com o código do país, por exemplo, '+5511999999999'
    kit.sendwhatmsg("+5511998995650", "Lembrete: Jantar no domingo!", 12, 0)

enviar_mensagem()
