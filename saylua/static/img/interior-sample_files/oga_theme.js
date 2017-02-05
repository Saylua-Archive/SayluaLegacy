/*
 *  oga_theme.js - functions specific to the OpenGameArt.org theme 
 *
 *  Written in 2009 by Bart Kelsey <bart@opengameart.org>
 *
 *  To the extent possible under law, the author(s) have dedicated all copyright and related 
 *  and neighboring rights to this software to the public domain worldwide. This software is 
 *  distributed without any warranty. 
 *
 *  You should have received a copy of the CC0 Public Domain Dedication along with this 
 *  software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
 */

(function($) {
  var oldWidth;
  var body_orig_width;
  var farright_orig_width;

  $(window).resize(function() {
    resize_bar(false);
  });

  $(function() {
    oldWidth = 0;
    body_orig_width = $('body').width();
    farright_orig_width = $('div#farright').width();
    resize_bar(true);
    $('.small-preview-title a').each(function() {
            var inner = $(this).html();
            if(inner.length > 16) {
                    inner = inner.substring(0, 15) + "...";
                    $(this).html(inner);
            }
    });

    $('.views-exposed-form select[multiple]').each(function() {
      replaceMultiSelect($(this));
    });

    $('.multi-select-replace input').click(function() {
      multiSelectToggle($(this));
    });

    $('.content').delegate('.play-button', 'click', function() {
      $('.stop-button').trigger('click');
      playButton(this);
    });

    $('.content').delegate('.stop-button', 'click', function() {
      stopButton(this);
    });

    $('.content').delegate('.subtree-toggle', 'click', function() {
      console.log('click');
      if($(this).hasClass('blank')) {
	    return;
      }
		
	  if($(this).hasClass('open')) {
	    $(this).removeClass('open').addClass('closed');
	  } else {
		$(this).removeClass('closed').addClass('open');
	  }
		
      $(this).parent().children('ul').slideToggle('fast');
    });
	
	$('.content').delegate('.art-preview-title', 'mouseenter', function() {
      $(this).addClass('hover');
    });
    
    $('.content').delegate('.art-preview-title', 'mouseleave', function() {
      $(this).removeClass('hover');
    });

    $('body').delegate('.view-art ul.pager a', 'click', function() {
      console.log('scroll to top');
      $('body').scrollTop(0);
    }); 
    
    $('input#edit-submit').click(function() {
      var clicked = $(this).attr('data-clicked');
      if(clicked) {
        return false;        
      } else {
        $(this).attr('data-clicked', 1);
      }
    });
  });

  function resize_right() {
    $('#right:not(.nosidebar)').each(function() {
      resize($(this), 350, 575);
    });

    $('.right-side').each(function() {
      resize($(this), 350, 575);
    });
    
    $('.nosidebar .right-column').each(function() {
      resize($(this), 350, 575);
    });
  }
  
  function resize_bar(initial) {
    var width = $(window).width(); 
    var threshold = 1260;
    if(width >= threshold && (initial || oldWidth < threshold)) {
      $('body').width(threshold);
      
      if(!$('#page').hasClass('wide')) $('div#farright').width(296);
      if($('#farright').length > 0 && !$('#page').hasClass('wide')) {
        $('#farright').appendTo('#maincontent');        
      } else {
        $('#right:not(.nosidebar)').width(890);
      }
    } else if((initial || oldWidth >= threshold) && width < threshold) {
      $('body').width(body_orig_width);
      if(!$('#page').hasClass('wide')) $('div#farright').width(farright_orig_width);
      if($('#farright').length > 0 && !$('#page').hasClass('wide')) {
        $('#farright').appendTo('#left');
      } else {
        $('#right:not(.nosidebar)').width(590);
      }
    }
    oldWidth = width;
  }
  
  function resize(element, margin, minWidth) {
    var parentWidth = element.parent().width();

    var newWidth = parentWidth - margin;
    if(newWidth < minWidth) {
      newWidth = minWidth;
    }

    element.width(newWidth - 20);
  }

  function stopButton(b) {
    $(b).addClass('play-button');
    $(b).removeClass('stop-button');


    b.audioElement.currentTime = 0;
    b.audioElement.pause();
  }

  function playButton(b) {
    $(b).addClass('stop-button');
    $(b).removeClass('play-button');

    if(!(b.audioElement)) {
      
      b.audioElement = document.createElement('audio');

      if(b.audioElement.canPlayType) {
        var url;
        if(b.audioElement.canPlayType('audio/ogg; codecs="vorbis"')) {
          url = $(b).attr('data-ogg-url');
        } else if(b.audioElement.canPlayType('audio/mpeg')) {
          url = $(b).attr('data-mp3-url');
        }
        
        b.audioElement.setAttribute('src', url);
        b.audioElement.load();
      } else {
        // flash fallback
      }
    }

    if(b.audioElement.canPlayType) {
      b.audioElement.play();
    } else {
      // flash fallback
    }
  }
  
  function replaceMultiSelect(item) {
    //console.log('replacing multi select');
    
    item.hide();
    var id = item.attr('id');
    var newid = "checkboxes-" + id;
    var html = "<div id='" + newid + "' class='multi-select-replace' data-select='" + id + "'>";
    
    item.find('option').each(function() {
      html += "<div class='multi-select-checkbox'><input type='checkbox' value='" + $(this).val() + "'";

      if($(this).attr('selected')) {
        html += " checked='checked'";
      }
      
      html += "> " + $(this).html() + "</div>";
    });
    
    html += "</div>";
    item.after(html);
  }

  function multiSelectToggle(item) {
    var id = item.parent().parent().attr('data-select');
    //console.log('id: ' + id);
    var select = $('#' + id);
    if(item.attr('checked')) {
      select.find("option[value=" + item.val() + "]").attr('selected', 'selected');
    } else {
      select.find("option[value=" + item.val() + "]").removeAttr('selected');
    }
  }
  

})(jQuery);
