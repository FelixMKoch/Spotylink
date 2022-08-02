const CLIENT_ID = "c5e017c3d86b4142aff199b492b0911e"
const SCOPE = "user-read-private user-read-email playlist-modify-private user-top-read"
const STATE_STRING_POSSIBLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
const GET_USER_IN_SESSION_URI = "https://createses.azurewebsites.net/api/get_users_in_session"
const GET_USER_INFO_URI = "https://saveuser.azurewebsites.net/api/get_user_info"
const SPOTIFY_REDIRECT_URI = "https://saveuser.azurewebsites.net/api/spotylink_auth?"
const SPOTIFY_LOGIN_URI = "https://accounts.spotify.com/authorize?response_type=code"
const CREATE_SESSION_URI ="https://createses.azurewebsites.net/api/spotylink-create-session"
const EXPORT_PLAYLIST_URI = "https://exportplay.azurewebsites.net/api/spotylink-export"
const SESSION_USER_TIMER_IN_MS = 5000
const USER_FOUND_TIMER_IN__MS = 2000

  
  function hide_login() {
    $("#login").css("display", "none");
    $("#loggedin").css("display", "block");
    $("#spotylink_image").css("display", "none")
  }
  
  function show_current_session() {
    $("#current_session").css("display", "block");
    $("#no_current_session").css("display", "none");
    $("#create_button_res").html("<b>Session-Key: </b>" + sessionStorage.getItem("session_id"))
    $("#session_input_things").css("display", "none")
    $("#session_export_things").css("display", "block")
  }
  
  function generate_random_string() {
    var text = '';
  
    for (var i = 0; i < 16; i++) {
      text += STATE_STRING_POSSIBLE.charAt(Math.floor(Math.random() * STATE_STRING_POSSIBLE.length));
    }
    return text;
  }
  
  
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  
  async function showSessionUsers() {
    show_current_session()
  
    while(true) {
      $.ajax({
        url: GET_USER_IN_SESSION_URI + "?sessionid=" + sessionStorage.getItem("session_id"),
        success: function(response) {
  
          json_obj = JSON.parse(response)
  
          newappend = ""
  
          for(username of json_obj) {
            row = document.createElement('tr');
            row.innerHTML = "<td>" + username +"</td>"
            newappend = newappend + "<tr><td>" + username + "</td></tr>"
          }
  
          $("#myTable tr").remove(); 
          $('#myTable').append(newappend)
  
        }
      });
  
      await(sleep(SESSION_USER_TIMER_IN_MS))
    }
  }
  
  async function wait_until_user_found() {
    do {
      $.ajax({
        url: GET_USER_INFO_URI + "?userid=" + sessionStorage.getItem("state_id"),
        success: function(response) {
  
          json_obj = JSON.parse(response)
          sessionStorage.setItem("user_id", json_obj.id)
  
          $("#displayname").html("<b>Name: </b>" + json_obj.display_name); 
          $("#front_email").html("<b>Email: </b>" + json_obj.email);
          $("#account_type").html("<b>Produkt: </b>" + json_obj.product);
          $("#hello_head").html("Hallo " + json_obj.display_name);
  
          hide_login()
  
        }
      });
  
      await sleep(USER_FOUND_TIMER_IN__MS)
    } while(sessionStorage.getItem("user_id") == null)
  }

  
  $("#login_button").click(function() {
    window.open(SPOTIFY_LOGIN_URI + "&state=" + sessionStorage.getItem("state_id") + "&client_id=" + CLIENT_ID + "&scope=" + SCOPE + "&redirect_uri=" + SPOTIFY_REDIRECT_URI)
  
    wait_until_user_found()
  });

  $("#hide_current_session_button").click(function() {
  
    hide_current_session()
  });

  $("#create_session_button").click(function() {
    var userid = sessionStorage.getItem("state_id")
  
    $.ajax({
      url: CREATE_SESSION_URI + "?userid=" + userid,
      success: function(response) {
  
        json_obj = JSON.parse(response);
  
        sessionStorage.setItem("session_id", json_obj.session_id)
        
        showSessionUsers()
  
      },
      error: function(response) {
        $("#create_button_fail").html("Konnte Session nicht erstellen")
        $("#create_button_fail").fadeOut(2500)

      }
  
    });
  })
  
  
  $("#join_session_button").click(function() {
    var session_id = $("#join_session_input").val()
    var userid = sessionStorage.getItem("state_id")
  
    $.ajax({
      url: CREATE_SESSION_URI + "?userid=" + userid + "&sessionid=" + session_id,
      success: function(response) {
  
        json_obj = JSON.parse(response);
  
        sessionStorage.setItem("session_id", json_obj.session_id)
  
        showSessionUsers()
  
      },
      error: function(response) {
        $("#create_button_fail").html("Konnte Session nicht joinen")
        $("#create_button_fail").fadeOut(2500)

      }
    });
  })
  
  
  $("#export_playlist_button").click(function() {
    var session_id = sessionStorage.getItem("session_id")
    var userid = sessionStorage.getItem("state_id")
  
    $.ajax({
      url: EXPORT_PLAYLIST_URI + "?userid=" + userid + "&sessionid=" + session_id,
      success: function(response) {
  
        $("#export_result_message").html("Playlist wurde erfolgreich exportiert!")
        $("#export_result_message").fadeOut(2500)
      },      
      error: function(response) {
        $("#create_button_fail").html("Konnte Export nicht durchführen")
        $("#create_button_fail").fadeOut(2500)
      }
    });
  })

  
  if(sessionStorage.getItem("state_id") == null){
    sessionStorage.setItem("state_id", generate_random_string())
  }
  else {
    wait_until_user_found()

    if(sessionStorage.getItem("session_id") !== null) {
      show_current_session()
    }
  }