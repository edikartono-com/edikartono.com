(function() {

   var TRANS_IMAGE_PATH = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
   var LAZY_CLASS_NAME = 'lazyload';
   
   CKEDITOR.plugins.add('lazyload', {
     
      requires : [ 'image', 'dialog' ], 
      icons: 'socialbox',
   
      init: function( editor ) {
   
         editor.dataProcessor.htmlFilter.addRules({
            elements: {
               img : function(element) {
                  if(element.attributes.class) {
                     if(element.attributes.class.indexOf(LAZY_CLASS_NAME) > -1) {
                        element.attributes.src = TRANS_IMAGE_PATH;
                     }
                  }
               }
            }
         });
         editor.dataProcessor.dataFilter.addRules({
            elements: {
               img : function(element) {
                  if(element.attributes.class) {
                     if(element.attributes.class.indexOf(LAZY_CLASS_NAME) > -1) {
                        element.attributes.src = element.attributes['data-src'];
                     }
                  }
               }
            }
         });
   
      }
   
   
   });
   
   CKEDITOR.on('dialogDefinition', function(ev) {
   
      var dialogName = ev.data.name;
      var dialogDefinition = ev.data.definition;
   
      if ( dialogName == 'image' ) {
   
         dialogDefinition.addContents({
            id : 'lazyLoad',
            label : 'Lazy Load',
            accessKey : 'M',
            elements : [
               {
                  id : 'lazyLoadCheck',
                  type : 'checkbox',
                  label : 'Apply lazy loading to this image?',
                  setup : function(type, element) {
   
                     var field = this;
   
                     field.setValue((element.getAttribute('data-src') !== null));
   
                  },
                  onChange: function() {
   
                     var dialog = this.getDialog();
                     var element = dialog.getSelectedElement();
                     var blnChecked = this.getValue();
                     var original = dialog.originalElement;
   
                     dialog.dontResetSize = true;
   
                     if(blnChecked) {
                        dialog.setValueOf('lazyLoad', 'lazyLoadDataOrig', original.getAttribute('src'));
                        dialog.setValueOf('info', 'txtUrl', TRANS_IMAGE_PATH);
                     } else {
                        dialog.setValueOf('lazyLoad', 'lazyLoadDataOrig', '');
                        if(element.hasAttribute('data-src')) {
                           dialog.setValueOf('info', 'txtUrl', original.getAttribute('data-src'));
                        } else {
                           dialog.setValueOf('info', 'txtUrl', original.getAttribute('src'));
                        }
                     }
   
                  },
                  commit: function(type, element) {

                     if(this.getValue() && !element.hasAttribute('data-src')) {

                        var dialog = this.getDialog();
                        var parentDialog = dialog.getParentEditor();
                        var original = dialog.originalElement;
   
                        element.setAttribute('data-src', dialog.getValueOf('lazyLoad', 'lazyLoadDataOrig'));
                        element.removeAttribute('src'); 
                        element.setAttribute('src', TRANS_IMAGE_PATH);
                        element.addClass(LAZY_CLASS_NAME);
   
                        original.setAttribute('src', TRANS_IMAGE_PATH); 
   
                     }
   
                     if(!this.getValue() && element.hasAttribute('data-src')) {

                        element.setAttribute('src', element.getAttribute('data-src')); 
                        element.removeAttribute('data-src');
                        element.removeClass(LAZY_CLASS_NAME);
   
                     }
                        
                  }
               },
               {
                  id : 'lazyLoadDataOrig',
                  type : 'text',
                  label : 'The image url for lazy loading (attribute data-src).',
                  setup : function(type, element) {
                     
                     var field = this;
                 
                     field.setValue((element.getAttribute('data-src') !== null) ? element.getAttribute('data-src') : '');
   
                  }
               }
            ]
         });
   
      }
   
   });

})();