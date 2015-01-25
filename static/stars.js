//source: http://rog.ie/blog/css-star-rater !-->
$(':radio').change(
  function(){
    $('.choice').text( this.value + ' stars' );
  } 
)