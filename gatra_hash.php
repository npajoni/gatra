
<?php

function gatra_get_hash_json ($valid_host)
{
    $now_ts = time();
    $hash   = md5($valid_host . (string)$now_ts);

    $data = array(
	       'host' => $valid_host,
               'ttl'  => 7200, 
	       'hash' => $hash		        	
           );
    return json_encode( $data );
}



function gatra_post_auth_hash ($url, $valid_host)
{ 
    $ch = curl_init($url);

    $data = gatra_get_hash_json($valid_host);

    //Tell cURL that we want to send a POST request.
    curl_setopt($ch, CURLOPT_POST, 1);
   
    curl_setopt($ch, CURLOPT_VERBOSE, 0); 

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); 
    //Attach our encoded JSON string to the POST fields.
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
 
    //Set the content type to application/json
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json')); 
 
    //Execute the request
    $result = curl_exec($ch);
    $http_response =  curl_getinfo ($ch,CURLINFO_HTTP_CODE);
    if ($http_response == 201)
    {     
	return $result;
    } 
    return;
}

$flens = gatra_post_auth_hash('http://gatra.zolechamedia.net:8000/hash/', '192.168.1.1');

?>
