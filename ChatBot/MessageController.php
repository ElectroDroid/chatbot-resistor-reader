<!-- Tang-Si : Message Control -->

<?php
class MessageController{
	private $access_token='QyMQ2IBjXlWhRdYBo1IZ+xsTI6pdb6rhBlmhrpjhCxFr4rzZSZQQIkTPxGERynATkw7uqgqGWM43Tbm8hyslo3i7j+6t3AVO35/hw5RY08/rhxFKlTCi6albLDfvtvkPn5DOO7tKviyIcLMsPtZ5dgdB04t89/1O/w1cDnyilFU=';
    
    public function getMessage(){
		header('Content-Type: text/html; charset=utf-8');
		$content=file_get_contents('php://input');
		$events=json_decode($content,true);
		if(!is_null($events['events'])) {
			foreach($events['events'] as $event){
				if($event['type']=='message'&&$event['message']['type']=='text'){
					$text = $event['message']['text'];
					$replyToken = $event['replyToken'];
					$json_output=json_decode($text,true);
					
					if(strpos($json_output,'help')==!false){
						$textSend="ทำตามนี้ดูนะครับ";
					}else{
						$textSend="ขอโทษนะครับ ผมไม่เข้าใจที่คุณพูดเลย";
					}
					$this->sendMessage($textSend,$replyToken);
					break;
				}
			}
		}
    }

    public function sendMessage($textSend,$replyToken){
		$messages=[
			'type'=>'text',
			'text'=>$textSend
		];
		$url='https://api.line.me/v2/bot/message/reply';
		$data=[
			'replyToken'=>$replyToken,
			'messages'=>[$messages]
		];
		$post=json_encode($data);
		$headers=array('Content-Type: application/json','Authorization: Bearer '.$this->access_token);
		$ch=curl_init($url);
		curl_setopt($ch,CURLOPT_CUSTOMREQUEST,"POST");
		curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
		curl_setopt($ch,CURLOPT_POSTFIELDS,$post);
		curl_setopt($ch,CURLOPT_HTTPHEADER,$headers);
		curl_setopt($ch,CURLOPT_FOLLOWLOCATION,1);
		curl_exec($ch);
		curl_close($ch);
    }
}