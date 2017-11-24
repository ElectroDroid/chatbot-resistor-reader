<?php
	// Error Checking
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
	 
	// include composer autoload
	require_once '/vendor/autoload.php';
	 
	// Bot Setting
	require_once 'bot_settings.php';
	 
	// Database Setting
	//require_once("dbconnect.php");


	use LINE\LINEBot;
	use LINE\LINEBot\HTTPClient;
	use LINE\LINEBot\HTTPClient\CurlHTTPClient;
	//use LINE\LINEBot\Event;
	//use LINE\LINEBot\Event\BaseEvent;
	//use LINE\LINEBot\Event\MessageEvent;
	use LINE\LINEBot\MessageBuilder;
	use LINE\LINEBot\MessageBuilder\TextMessageBuilder;
	use LINE\LINEBot\MessageBuilder\StickerMessageBuilder;
	use LINE\LINEBot\MessageBuilder\ImageMessageBuilder;
	use LINE\LINEBot\MessageBuilder\LocationMessageBuilder;
	use LINE\LINEBot\MessageBuilder\AudioMessageBuilder;
	use LINE\LINEBot\MessageBuilder\VideoMessageBuilder;
	use LINE\LINEBot\ImagemapActionBuilder;
	use LINE\LINEBot\ImagemapActionBuilder\AreaBuilder;
	use LINE\LINEBot\ImagemapActionBuilder\ImagemapMessageActionBuilder ;
	use LINE\LINEBot\ImagemapActionBuilder\ImagemapUriActionBuilder;
	use LINE\LINEBot\MessageBuilder\Imagemap\BaseSizeBuilder;
	use LINE\LINEBot\MessageBuilder\ImagemapMessageBuilder;
	use LINE\LINEBot\MessageBuilder\MultiMessageBuilder;
	use LINE\LINEBot\TemplateActionBuilder;
	use LINE\LINEBot\TemplateActionBuilder\DatetimePickerTemplateActionBuilder;
	use LINE\LINEBot\TemplateActionBuilder\MessageTemplateActionBuilder;
	use LINE\LINEBot\TemplateActionBuilder\PostbackTemplateActionBuilder;
	use LINE\LINEBot\TemplateActionBuilder\UriTemplateActionBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateMessageBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\ButtonTemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\CarouselTemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\CarouselColumnTemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\ConfirmTemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\ImageCarouselTemplateBuilder;
	use LINE\LINEBot\MessageBuilder\TemplateBuilder\ImageCarouselColumnTemplateBuilder;
	 
	// Connect LINE Messaging API
	$httpClient = new CurlHTTPClient(LINE_MESSAGE_ACCESS_TOKEN);
	$bot = new LINEBot($httpClient, array('channelSecret' => LINE_MESSAGE_CHANNEL_SECRET));
	 
	// Get value LINE Messaging API
	$content = file_get_contents('php://input');
	 
	// Change "JSON" to "array"
	$events = json_decode($content, true);
	if(!is_null($events)){
		$replyToken = $events['events'][0]['replyToken'];
	    $typeMessage = $events['events'][0]['message']['type'];
	    $userMessage = $events['events'][0]['message']['text'];
	    switch ($typeMessage){
	        case 'text':
	            switch ($userMessage) {
	                case "Hello":
	                    $textReplyMessage = "Hello! Let's me help you read resistor color bar.";
	                    $replyData = new TextMessageBuilder($textReplyMessage);
	                    break;
	                
	                case "help":
	         //        	$textReplyMessage = "Sorry, Tang-Si is sleeping now."
	         //        	$textMessage = new TextMessageBuilder($textReplyMessage);
	                	
	                	$stickerID = 1;
	                	$packageID = 1;
	                	$replyData = new StickerMessageBuilder($packageID,$stickerID);	
	                	
	         //        	//Multimessage replying
	         //        	$multiMessage = new MultiMessageBuilder;
	         //        	$multiMessage->add($textMessage);
	         //        	$multiMessage->add($stickerMessage);
   	 					// $replyData = $multiMessage;                  
	                	break;
	                	
	                default:
	                    $textReplyMessage = "Sorry, I don't know what are you talking about?";
	                    $replyData = new TextMessageBuilder($textReplyMessage);
	                    break;                                      
	            }
	            break;
	        default:
	            $textReplyMessage = json_encode($events);
	            $replyData = new TextMessageBuilder($textReplyMessage);  
	            break;  
	    }
	}

	//Prepare message for replying
	//$textMessageBuilder = new TextMessageBuilder($textReplyMessage);
	 
	//Reply message
	$response = $bot->replyMessage($replyToken,$replyData);


	echo "Tang-Si is OK!";
?>