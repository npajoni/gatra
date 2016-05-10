var gatra_player = function(_player, _meta) 
{
    /* 
     *	url_post es la direccion donde se hace POST
     * de los datos
     */
    url_post = _meta.url_post;
    
    try {
	_data = {
	    title : _meta.title,
	    season : _meta.season,
	    episode : _meta.episode,
	    device_type : _meta.device,
	    user_name : _meta.user_name,
	    user_id: _meta.user_id,
	    duration: _meta.duration,
	    country : _meta.country,
	    idp: _meta.idp,
	    idp_name: _meta.idp_name,
	    media_id: _meta.media_id,
	    media_filename : '',
	    media_type: ''
	    };
	}
	catch(err) {
	    console.log(err);
	}
    /**
     * Send a post event
     */
    _sendEventPost = function (url, type, trigger) 
    {
	_config  = _player.getConfig();
	_item    = _player.getItemMeta();
	_quality = _player.getVisualQuality();
 
	
	_local_data = {
		type : type,
		trigger : trigger,
		width     : _quality.level.width,
		container_height : _config.containerHeight,
		container_width : _config.containerWidth,
		state	      : _config.state,
		position      : _player.getPosition(),
		fullscreen    : _config.fullscreen,
		volume        : _player.getVolume()
	      }; 

	if ('qualityLabel' in _config) {
	    _local_data.quality_label = _config.qualityLabel;
	}

	if ('segment' in _item) {
	    _local_data.bandwidth  = _item.segment.bandwidth;
	    _local_data.bitrate    = _item.segment.bitrate;
	    _local_data.load_time  = _item.segment.loadTime;
	    _local_data.media_seq  = _item.segment.mediaSequenceNumber;
	}


	jQuery.ajax({
	    type : 'POST',
	    url  : url,
	    headers : {
		'Gatra-Hash' : _meta.gatra_hash
	    },
	    contentType : 'application/json',
	    data : JSON.stringify(_local_data),
	    error : function(xhr, status, error ) {
		console.log(error);
	    }
	});
	
    }

    var _delta    = 10;		/* Number of seconds to post event */
    var _trigger  = 0;
    var _ticks    = 0;
    var _event_post_url;
    var _initial_check = 10;	/* Number of click */
    var _flag     = true;	/* Checking stage  */

    _start = 0;
    _t     = 0;


    /**
     * Return the number of ms to _initial_check clicks
     */
    _cf = function(needSum) {
	if (needSum) {
	    if (!_start) {
		_start = new Date();
	    }
	    _t = _t + 1;
	}
	else {
	    ms = new Date() - _start;
	    return ms; 
	}
    }

    /**
     * Handler to manage timer event
     */
    _timerEvent = function (event)
    {
	_ticks = _ticks + 1;
	if (_flag) {
	    if (_ticks != _initial_check) {
		_cf(true);
	    }
	    else {
		_trigger = Math.ceil(_delta * 1000 * _initial_check / _cf(false));
		_flag = false;
	    }
	}
	else {
	    if (_ticks === _trigger) {
		_ticks = 0;
		_sendEventPost(_event_post_url, 'Playing', 'timer');
	    }
	} 
    }
    

    _player.on('firstFrame',function() {
	_source = _player.getPlaylistItem();
	_data.media_filename = _source.file;
	_data.media_type     = _source.sources[0].type
	
	jQuery.ajax({
	    type : 'POST',
	    url :   url_post,
    	    headers : {
		'Gatra-Hash' : _meta.gatra_hash
	    },
	    contentType: 'application/json',
	    data : JSON.stringify(_data),

	    success : function(response) {
		_event_post_url = response.location;
		_player.on('time', _timerEvent);
	    },
	    error : function(xhr, status, error ) {
		console.log(status);
	    }
	}); 
    });
}


