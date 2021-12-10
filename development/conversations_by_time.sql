select 
    conversations.id, 
    conversations.initiator_id, 
    conversations.participant_id, 
    conversations.subject, 
    conversations.offer_id, 
    max(messages.timestamp) as latest_message_time,
    (
        select messages.body 
        from messages 
        where messages.conversation_id == conversations.id 
        order by timestamp desc limit 1
    ) as latest_message_body
from conversations 
    inner join messages on messages.conversation_id=conversations.id 
group by conversations.id 
order by latest_message_time desc;