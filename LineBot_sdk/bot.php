<?php
	// Error Checking
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
	 
	// include composer autoload
	require_once '../vendor/autoload.php';
	 
	// Setting Bot
	require_once 'bot_settings.php';
	 
	//Database Connection
	//require_once("dbconnect.php");
	 
	///////////// Class
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
	 
	//Connect LINE Messaging API
	$httpClient = new CurlHTTPClient(LINE_MESSAGE_ACCESS_TOKEN);
	$bot = new LINEBot($httpClient, array('channelSecret' => LINE_MESSAGE_CHANNEL_SECRET));
	 
	//Get value LINE Messaging API
	$content = file_get_contents('php://input');
	 
	//Change "JSON" to "Array"
	$events = json_decode($content, true);
	
	//create "replyToken" when has event
	if(!is_null($events)){
	    $replyToken = $events['events'][0]['replyToken'];
	}
	//Prepare text for replying
	$textMessageBuilder = new TextMessageBuilder(json_encode($events));
	 
	//Reply message
	$response = $bot->replyMessage($replyToken,$textMessageBuilder);
	if ($response->isSucceeded()) {
	    echo 'Succeeded!';
	    return;
	}
	 
	// Failed
	echo $response->getHTTPStatus() . ' ' . $response->getRawBody();
?>