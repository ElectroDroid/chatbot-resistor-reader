<?php
	// Error Checking
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
	 
	// include composer autoload
	require_once '/vendor/autoload.php';
	 
	// Bot Setting
	require_once 'bot_settings.php';
	 
	//require_once '../src/resRead.py';
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
		$userID = $events['events'][0]['source']['userId'];
	    // $typeMessage = $events['events'][0]['message']['type'];
	    // $userMessage = $events['events'][0]['message']['text'];

	    if(isset($events['events'][0]) && array_key_exists('message',$events['events'][0])){
        $is_message = true;
        $typeMessage = $events['events'][0]['message']['type'];
        $userMessage = $events['events'][0]['message']['text'];     
        $idMessage = $events['events'][0]['message']['id']; 
    	}


	    switch ($typeMessage){
	        case 'text':
	            switch ($userMessage) {
	                case "Hello" :
	                case "hello" :
	                case "Hi" :
	                case "hi" :
	                	//Emoji
	                	$code = '10000B'; //Emoji Code
						$bin = hex2bin(str_repeat('0', 8 - strlen($code)) . $code);
						$emoticon =  mb_convert_encoding($bin, 'UTF-8', 'UTF-32BE');

	                    $textReplyMessage = "Hello! Let's me help you read resistor color bar. Type \"help\" to see how I can help you $emoticon";
	                    $replyData = new TextMessageBuilder($textReplyMessage);
	                break;
	                
	                case "Help" :
	                case "help" :
	                	$text1 = "Want me to help, right? Follow this!";
	                	$text2 = "1. Take a photo of resistor and send it to me";
	                	$text3 = "2. Wait and get your result!!!";
	                
	                	$stickerID = 144;
	                	$packageID = 2;	

	                	//$picFullSize = 'https://tangsibot.scm.azurewebsites.net/dev/wwwroot/Tangsi_Photo/Instruction-full';
                    	//$picThumbnail = 'https://tangsibot.scm.azurewebsites.net/dev/wwwroot/Tangsi_Photo/Instruction-thumbnail';
	                	
	                	//Multipel Message Setting
	                	$multiMessage = new MultiMessageBuilder();

	                	$multiMessage->add(new TextMessageBuilder($text1, $text2, $text3))
	                				 ->add(new StickerMessageBuilder($packageID,$stickerID));
	                				 
	                	$replyData = $multiMessage;
	               	break;
	                	
	                default:
	                    $textReplyMessage = "Sorry, I don't know what are you talking about?";
	                    $replyData = new TextMessageBuilder($textReplyMessage);
	                break;                                      
	            }
	        break;
	        // Receive image
	        case (preg_match('/[image]/',$typeMessage) ? true : false) :
                $response = $bot->getMessageContent($idMessage);
                if ($response->isSucceeded()) {
                    // คำสั่ง getRawBody() ในกรณีนี้ จะได้ข้อมูลส่งกลับมาเป็น binary 
                    // เราสามารถเอาข้อมูลไปบันทึกเป็นไฟล์ได้
                    $dataBinary = $response->getRawBody(); // return binary
                    
           			//          $dataHeader = $response->getHeaders();
        			// $replyData = new TextMessageBuilder(json_encode($dataHeader));

                    // ดึงข้อมูลประเภทของไฟล์ จาก header
                    $fileType = $response->getHeader('Content-Type');                           
                    list($typeFile,$ext) = explode("/",$fileType);
                    $ext = ($ext=='jpeg' || $ext=='jpg')?"jpg":$ext;
                    $fileNameSave = time().".".$ext;
                    
                    $botDataFolder = 'image/';
                    if(!file_exists($botDataFolder)) { // ตรวจสอบถ้ายังไม่มีให้สร้างโฟลเดอร์ image
                        mkdir($botDataFolder, 0777, true);
                    }                                                     
                    $botDataUserFolder = $botDataFolder.$userID; // มีโฟลเดอร์ด้านในเป็น userId อีกขั้น
                    if(!file_exists($botDataUserFolder)) { // ตรวจสอบถ้ายังไม่มีให้สร้างโฟลเดอร์ userId
                        mkdir($botDataUserFolder, 0777, true);
                    }   

                    // กำหนด path ของไฟล์ที่จะบันทึก
                    $fileFullSavePath = $botDataUserFolder.'/'.$fileNameSave;
                    file_put_contents($fileFullSavePath,$dataBinary); // ทำการบันทึกไฟล์


                	$path = $fileFullSavePath;
    				//$value = exec("cv2 && python ../src/resRead.py $path");
    				//$item = 'python';
    				$value = exec("cv && python ../src/test.py $path");

                    //$picFullSize = 'https://tangsibot.scm.azurewebsites.net/dev/wwwroot/LineBot_sdk/image/$userID/$fileNameSave';
                    //$picThumbnail = 'https://tangsibot.scm.azurewebsites.net/dev/wwwroot/LineBot_sdk/image/$userID/$fileNameSave';

                    $text1 = "I've gotten your image already. Please, wait for a while to get your result.";
                    $text2 = $value;

                    $multiMessage = new MultiMessageBuilder();

                    $multiMessage->add(new TextMessageBuilder($text1))
                    			 ->add(new TextMessageBuilder($text2));
	                //$multiMessage->add(new TextMessageBuilder($textReplyMessage))
	                //			 ->add(new ImageMessageBuilder($picFullSize,$picThumbnail));
	                $replyData = $multiMessage;

                    //$replyData = new TextMessageBuilder($textReplyMessage);
                    
                    break;
              	}
                
                //$failMessage = json_encode($idMessage.' '.$response->getHTTPStatus() . ' ' . $response->getRawBody());
                $failMessage = "Sorry, I can't save your image. Please send a jpg or jpeg image";
                $replyData = new TextMessageBuilder($failMessage);  
            break;                                                      
	        
	        default:
	            $textReplyMessage = json_encode($events);
	            $replyData = new TextMessageBuilder($textReplyMessage);  
	        break;  
	    }

	    //Prepare message for replying
		//$textMessageBuilder = new TextMessageBuilder($textReplyMessage);
	 
		//Reply message
		$response = $bot->replyMessage($replyToken,$replyData);
		//unlink($fileFullSavePath);
	}

	echo "Tang-Si is OK!";
?>