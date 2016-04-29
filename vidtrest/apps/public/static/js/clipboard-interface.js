// copy to Clipboard
new Clipboard("#copytoclipboard");
var $copybutton = $('#copytoclipboard').tooltip({
  animation: true,
  delay: { "show": 200, "hide": 200 },
  trigger: 'click',
  placement: 'bottom'
});
$copybutton.on('mouseleave', function() {
  if ($(this).attr('aria-describedby') !== undefined) {
    $(this).click();
  }
});