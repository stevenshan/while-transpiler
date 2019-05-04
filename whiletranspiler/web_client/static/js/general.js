$(function() {

  var default_filename = "Untitled file";

  var parse_req_id = undefined;
  var save_callbacks = [];

  const socket = io(window.location.href);

  $(".tabs").tabs();

  socket.on('disconnect', function() {
    socket.open();
  });

  function set_editor_readonly(_editor) {
    _editor.setOptions({
      readOnly: true,
      highlightActiveLine: false,
      highlightGutterLine: false
    });
    _editor.renderer.$cursorLayer.element.style.display = "none"
  }

  function setup_editor(name) {
    var _editor = ace.edit(name)
    var _session = _editor.getSession();
    _session.setMode("ace/mode/c_cpp");
    _editor.renderer.setScrollMargin(10, 10);
    return _editor;
  }

  var editor = setup_editor("editor");
  var editor_highlight_marker = undefined;

  var c_code_editor = setup_editor("c-code-editor");
  set_editor_readonly(c_code_editor);

  var ast_editor = setup_editor("ast-editor");
  set_editor_readonly(ast_editor);

  var tokens_editor = setup_editor("tokens-editor");
  set_editor_readonly(tokens_editor);

  function set_editor_value(_editor, string) {
    _editor.setValue(string, 1);
  }

  editor.commands.addCommand({
    name: 'saveFile',
    bindKey: {
      win: 'Ctrl-S',
      mac: 'Command-S',
      sender: 'editor|cli'
    },
    exec: function() { save(); },
  });

  editor.session.on('change', function() {
    $("#results-tabs .tab-body").addClass("staging");
  });

  var last_used_filename = undefined;
  var current_filename = undefined;
  function change_filename(new_name) {
    if (new_name === undefined || new_name === null) {
      return;
    }

    new_name = $.trim(new_name);
    if (new_name == "") {
      new_name = default_filename;
    }

    if (new_name == current_filename) {
      return;
    }

    last_used_filename = current_filename;
    current_filename = new_name;
    $("#filename-text").text(current_filename);
    $("#filename-input").val(current_filename);
    setCookie("filename",
        current_filename == default_filename ? "" : current_filename);

    socket.emit("loadfile", current_filename);
  }

  function run_transpiler(execute) {
    execute = execute || false;
    parse_req_id = random_id();
    socket.emit("build", {
      filename: current_filename,
      req_id: parse_req_id,
      execute: execute,
    });
    $("#results-tabs .tab-content").addClass("loading");
  }

  $("#filename-input")
    .on("keydown", function(e) {
      if (e.keyCode == 13) {
        $(this).blur();
      }
    })
    .focus(function() {
      $(this).val(current_filename || default_filename);
    })
    .blur(function() {
      change_filename($(this).val());
    });

  var saved_filename = getCookie("filename");
  var _set_filename = ($.trim(saved_filename) == "" ?
      default_filename : saved_filename);

  change_filename(_set_filename);

  $("#fileselect-modal").modal({
    onOpenStart: function() {
      $("#fileselect-modal .progress").css("display", "");
      $("#fileselect-modal-content").html("");
      socket.emit("filelisting");
    }
  });

  window.select_file = function(filename) {
    M.Modal.getInstance($("#fileselect-modal")).close();
    change_filename(filename);
  }

  window.save = function() {
    socket.emit("save", {
      text: editor.getValue(),
      filename: current_filename,
    });
    save_callbacks.push(run_transpiler);
  };

  window.execute = function() {
    socket.emit("save", {
      text: editor.getValue(),
      filename: current_filename,
    });
    save_callbacks.push(function() {
      run_transpiler(true);
    });
  }

  socket.on("filelisting", function(e) {
    $("#fileselect-modal .progress").css("display", "none");

    var html = '';
    e.forEach(function(elem) {
      html += '<a onclick="select_file(\'' + elem + '\')">' + elem + '</a>';
    });

    $("#fileselect-modal-content").html(html);
  });

  socket.on("filedata", function(data) {
    if (data.error === true && data.reason === "unopenable") {
      M.toast({html: "Cannot open this file."});
      if (last_used_filename !== default_filename) {
        change_filename(last_used_filename);
      }
      return;
    }

    var string = "";
    if (data.error === false && current_filename === data.filename) {
      string = data.text || string;
    }

    if (data.error && data.reason === "notfound") {
      return;
    }

    set_editor_value(editor, string);
    run_transpiler();
  });

  socket.on("savestatus", function(data) {
    if (data) {
      // error
      M.toast({html: "Failed to save file."});
    } else {
      // no error
    }
    while (save_callbacks.length > 0) {
      save_callbacks.pop()();
    }
  });

  socket.on("transpiler_c_code", function(data) {
    if (parse_req_id !== data.req_id) {
      return;
    }

    var $tab = $("#c-code-tab");

    $tab
      .removeClass("loading")
      .toggleClass("error", data.error);

    if (!data.error) {
      set_editor_value(c_code_editor, data.text || "");
    }

    $tab.find(".tab-body").removeClass("staging");

  });

  socket.on("transpiler_ast", function(data) {
    if (parse_req_id !== data.req_id) {
      return;
    }

    var $tab = $("#ast-tab");

    $tab
      .removeClass("loading")
      .toggleClass("error", data.error);

    if (!data.error) {
      set_editor_value(ast_editor, data.text || "");
    }

    $tab.find(".tab-body").removeClass("staging");

  });

  socket.on("transpiler_tokens", function(data) {
    if (parse_req_id !== data.req_id) {
      return;
    }

    var $tab = $("#tokens-tab");

    $tab
      .removeClass("loading")
      .toggleClass("error", data.error);

    if (!data.error) {
      set_editor_value(tokens_editor, data.text || "");
    }

    $tab.find(".tab-body").removeClass("staging");

  });

  socket.on("parsestatus", function(data) {
    if (editor_highlight_marker !== undefined) {
      editor.session.removeMarker(editor_highlight_marker);
    }

    if (data !== undefined && data.error) {
      var error_line = parseInt(data.line);
      if (isNaN(error_line)) {
        return;
      }

      error_line -= 1;

      var marker = editor.session.addMarker(
          new ace.Range(error_line, 0, error_line, 1),
          'ace_error-marker', 'fullLine');

      editor_highlight_marker = marker;
    }
  });

  $("#execution-modal").modal();
  var execution_modal = M.Modal.getInstance($("#execution-modal"));

  socket.on("execution", function(data) {
    if (parse_req_id !== data.req_id) {
      return;
    }

    if (!execution_modal.isOpen) {
      execution_modal.open();
    }

    var $content = $("#execution-modal-content");

    if (data.signal === "start") {
      $content.empty();
    }

    $("#execution-modal").toggleClass("loading", data.signal !== "end");

    if (data.message !== undefined && data.message != "") {
      $content.append($(
        '<div class="execution-message"><pre>' + data.message + '</pre></div>'
      ));
    }

  });

});


