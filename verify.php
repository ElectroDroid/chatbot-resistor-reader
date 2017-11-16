<?php
$access_token = 'QyMQ2IBjXlWhRdYBo1IZ+xsTI6pdb6rhBlmhrpjhCxFr4rzZSZQQIkTPxGERynATkw7uqgqGWM43Tbm8hyslo3i7j+6t3AVO35/hw5RY08/rhxFKlTCi6albLDfvtvkPn5DOO7tKviyIcLMsPtZ5dgdB04t89/1O/w1cDnyilFU=';

$url = 'https://api.line.me/v1/oauth/verify';

$headers = array('Authorization: Bearer ' . $access_token);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
$result = curl_exec($ch);
curl_close($ch);

echo $result;