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

      myCodeMirror.addKeyMap({
          'Ctrl-R': function (cm) {
              exec_sql()
          },
          'Cmd-R': function (cm) {
              exec_sql()
          },
          'Ctrl-F': function (cm) {
              format_sql()
          },
          'Cmd-F': function (cm) {
              format_sql()
          }
      });


  });
}

//显示双击选中的表信息
function showTableDesc(event, treeId, treeNode){
    console.log(treeNode ? treeNode.tId + ", " + treeNode.name : "isRoot");
    if(treeNode.getParentNode()){
        $('#table_info_model').modal({
          keyboard: true
        })

        $.post("/dbmaster/table_desc/",{
            "table_schema" : treeNode.getParentNode().name,
            "table_name" : treeNode.name
        },function(data){
            console.log(data)
            columns = data.data;
            html=""
            for (i in columns){
                html +="<tr>";
                html +="<td>"+columns[i][0]+"</td>";
                html +="<td>"+columns[i][1]+"</td>";
                html +="<td>"+columns[i][2]+"</td>";
                html +="<td>"+columns[i][3]+"</td>";
                html +="<td>"+columns[i][4]+"</td>";
                html +="<td>"+columns[i][5]+"</td>";
                html +="<td>"+columns[i][6]+"</td>";
                html +="<td>"+columns[i][7]+"</td>";
                html +="</tr>";
            }
            $("#table-info-box").html(html);
        });
    }

}


function loadDatabaseTree(){
  $.post("/dbmaster/znode_content/",function(data){
    console.log(data);
    var zTreeObj;
    // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
    var setting = {
        callback: {
            onDblClick: showTableDesc
        }
    };
    // zTree 的数据属性，深入使用请参考 API 文档（zTreeNode 节点数据详解）
    var zNodes = data.data
    $(document).ready(function(){
      zTreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
    });
  });
}

function build_nav_tabs(resultlist){
    html = "";
    for (i in resultlist){
        name = "结果集"+i
        if(i ==0 ){
            html += "<li role='presentation' class='active'><a href='#"+name+"' aria-controls='"+name+"' role='tab' data-toggle='tab'>"+name+"</a></li>"
        }else{
            html += "<li role='presentation'><a href='#"+name+"' aria-controls='"+name+"' role='tab' data-toggle='tab'>"+name+"</a></li>"
        }
    }

    return html
}


function build_tab_content(resultlist){
    html = "";
    for (i in resultlist){
        data = resultlist[i]
        name = "结果集"+i
        content = ''
        content +='<div class="breadcrumb"><small>执行时间 : <strong>'+data.cost_time+' sec </strong> &nbsp;&nbsp;条数 : <strong>'+data.rowcount+'条</strong></small></div>'
        content +='<table class="table table-bordered">'
        content +='<tr class="success">'
        content += "</tr>"
        for (j in data.titles) {
            content += "<td>";
            content += data.titles[j][0];
            content += "</td>";
        }
        content += '<tbody>'
        for (j in data.result_set) {
            content += "<tr>";
            for (k in data.titles) {
                content += "<td>";
                content += data.result_set[j][k];
                content += "</td>";
            }
            content += "</tr>";
        }
        content += '</tbody>'
        content +='</table>'
        if(i==0){
            html += '<div role="tabpanel" class="tab-pane active" id="'+name+'">'+content+'</div>'
        }else{
            html += '<div role="tabpanel" class="tab-pane" id="'+name+'">'+content+'</div>'
        }
    }

    return html
}


function exec_sql(){

    var sql_content = myCodeMirror.getValue();

    if(sql_content.trim() == ''){
        alert("SQL 内容 不能为空!");
        return;
    }

    $("#tab-content").html("<p>正在执行,请稍等....</p>")
    $( "#btn_exec_sql" ).prop( "disabled", true );


    $.post("/dbmaster/db_execute/",{
        "sql_content" : sql_content
    },function(data){
        $( "#btn_exec_sql" ).prop( "disabled", false );

        console.log(data)
        if(data.code == 500){
            $("#title_box").html()
            $("#exec_result_box").html("<p style='padding:10px' class='text-danger'>执行失败,错误信息如下:<br/>"+data.message+"</p>")
        }else {
            nav_tabs_html = build_nav_tabs(data.data)
            tab_content = build_tab_content(data.data)

            $("#nav-tabs").html(nav_tabs_html)
            $("#tab-content").html(tab_content)
        }

    });
}


function exec_selected_sql(){
    var sql_content = myCodeMirror.getSelection();

    if(sql_content.trim() == ''){
        alert("SQL 内容 不能为空!");
        return;
    }
    $("#tab-content").html("<p>正在执行,请稍等....</p>")
    $( "#btn_exec_sql" ).prop( "disabled", true );


    $.post("/dbmaster/db_execute/",{
        "sql_content" : sql_content
    },function(data){
        $( "#btn_exec_sql" ).prop( "disabled", false );

        console.log(data)
        if(data.code == 500){
            $("#title_box").html()
            $("#exec_result_box").html("<p style='padding:10px' class='text-danger'>执行失败,错误信息如下:<br/>"+data.message+"</p>")
        }else {
            nav_tabs_html = build_nav_tabs(data.data)
            tab_content = build_tab_content(data.data)

            $("#nav-tabs").html(nav_tabs_html)
            $("#tab-content").html(tab_content)
        }

    });
}


function format_sql(){
    var sql_content = myCodeMirror.getValue();

    if(sql_content.trim() == ''){
        alert("SQL 内容 不能为空!");
        return;
    }
    $.post("/dbmaster/sql_format/",{
        "sql_content" : sql_content
    },function(data){
        console.log(data)
        if(data.code == 200){
            myCodeMirror.setValue(data.data)
        }
    });
}


initCodeMirror()
loadDatabaseTree()

