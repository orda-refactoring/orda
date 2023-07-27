ClassicEditor
.create(document.querySelector('#content'), {
  language: 'ko',
})
.then(editor => {
  editor.model.document.on('change:data', () => {
    document.querySelector('#content').value = editor.getData();
  });
})
.catch(error => {
  console.error(error);
});

// 툴바 커스텀
CKEDITOR.editorConfig = function( config ) {
  config.toolbarGroups = [
    { name: 'insert', groups: [ 'insert' ] },
    { name: 'styles', groups: [ 'styles' ] },
    { name: 'colors', groups: [ 'colors' ] },
    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
    { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
    { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
    { name: 'forms', groups: [ 'forms' ] },
    '/',
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
    { name: 'links', groups: [ 'links' ] },
    '/',
    { name: 'tools', groups: [ 'tools' ] },
    { name: 'others', groups: [ 'others' ] },
    { name: 'about', groups: [ 'about' ] }
  ];

  config.removeButtons = 'Source,Save,NewPage,Preview,Print,Templates,Cut,Copy,Paste,PasteFromWord,PasteText,Find,Replace,Undo,Redo,SelectAll,Scayt,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,CopyFormatting,RemoveFormat,Flash,Table,HorizontalRule,Smiley,SpecialChar,PageBreak,Iframe,Link,Language,Anchor,Unlink,BidiRtl,BidiLtr,Blockquote,CreateDiv,Indent,Outdent,Superscript,Subscript,Bold,Italic,Underline,Strike,Maximize,About,ShowBlocks';
};