[actor] @dbtype:fs
    """
    Email sender
    """
    method:send @tags: noauth
        var:sender_name str,, Sender full name @optional
        var:sender_email str,, Sender email
        var:receiver_email str,, Receiver email.
        var:subject str,, Email subject
        var:body str,, Email body
        result:str