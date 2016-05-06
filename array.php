<?php

function __get_media_urls($cdn, $media_id, $query_url)
{
    return array( 'failback_type' => 'mp4',
		  'primary_type'  => 'hls',
		  'primary_video' => $cdn . $media_id . '/hls/' . $media_id . '.m3u8',
		  'fb_low_quality'    => $cdn . $media_id . '/mp4/' . $media_id . '/350/' .  $media_id . '.mp4',
		  'fb_medium_quality' => $cdn . $media_id . '/mp4/' . $media_id . '/800/' .  $media_id . '.mp4',
		  'fb_high_quality'   => $cdn . $media_id . '/mp4/' . $media_id . '/1200/' . $media_id . '.mp4' );
}

print_r (__get_media_urls('http://cdnlevel3.zolechamedia.net/', '008114', ''));

?>