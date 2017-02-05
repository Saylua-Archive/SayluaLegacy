(function ($) {
  $(function() {
    $('body').delegate('[data-fid]', 'mouseup', function() {
      var fid = $(this).attr('data-fid');
      var url = '/file/' + fid + '/dlcounter';
      $.ajax({ 
        url: url,
        success: function(data, textStatus, jqXHR) {
          console.log(data);
          $('span#dlcount-' + fid).html(data.dlcount);
        }
      });
      return true;
    });
  });
})(jQuery);