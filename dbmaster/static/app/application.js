/**
 * Created by xiexiyang on 17/3/29.
 */
var  myCodeMirror;

function initCodeMirror(){
  myTextArea = document.getElementById("sql_content")

  $.post("/dbmaster/hint_content/",function(data) {
      myCodeMirror = CodeMirror.fromTextArea(myTextArea, {
          mode: "text/x-mysql",
          value:"SELECT * FROM qding_platform.order_base limit 5",
          lineNumbers: true,
          extraKeys: {Tab: "autocomplete"}, // To invoke the auto complete
          hint: CodeMirror.hint.sql,
          hintOptions: {
              tables: data.data
          }
      });

      //myCodeMirror.setValue("SELECT * FROM qding_platform.order_base limit 5")
  });
}

function new_application(){
    var reason = $("#reason").val()
    var sql_content = myCodeMirror.getValue();

    if(sql_content.trim() == ''){
        alert("SQL 内容 不能为空!");
        return;
    }
    $.post("/dbmaster/new_update_application/",{
        "reason" : reason,
        "sql_content" : sql_content
    },function(data){
        history.go(-1)
    });
}


initCodeMirror()

