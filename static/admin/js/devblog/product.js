window.addEventListener('load', function(){
    "use strict";
    const prod_typ = $("#id_product_typ").val();
    
    function prodTyp(typ){
        if (typ == 2) {
            $("#id_schedule_payment").val(0).change();
            $("#id_schedule_payment option").each(function(){
                if (this.selected == false){
                    $(this).prop('disabled', true);
                } else {
                    $(this).attr('selected', true);
                };
            });
        } else {
            $("#id_schedule_payment option").each(function(){
                $(this).removeAttr('disabled');
            });
        }
    };

    prodTyp(prod_typ);

    $("#id_product_typ").on("change", function(){
        const typ = $(this).val();
        prodTyp(typ);
    });
})

