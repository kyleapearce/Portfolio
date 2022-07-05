// background script
var data = {
    // "term1": {
    //     "definition": "def for term 1",
    //     "link": "www.link1.com",
    // },
    // "term2": {
    //     "definition": "term 2 def",
    //     "link": "www.link2.com",
    // }
}

var temp_term = "NO TEMP YET";

function setTempTerm(term) {
    temp_term = term;
}

function add_term(definition, link) {
    data[temp_term] = {
        "definition": definition,
        "link": link
    }
    console.log(data);
}

function get_definition(term) {
    return data[term].definition;
}

function get_link(term) {
    return data[term].link;
}

function print_terms() {
    var arrTerms = [];
    index = 0;
    for (const [key, value] of Object.entries(data)) {
        console.log(key, value);
        arrTerms[index] = value;
        index++;
    }
    return arrTerms;
}

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";

    var term_list = document.getElementById('term_list_id');
    term_list.innerHTML = "";

    for (const [key, value] of Object.entries(data)) {
        var term = document.createElement('a');
        // term.onclick = ;
        var term_text = document.createTextNode(key);
        term.appendChild(term_text);
        term_list.appendChild(term);
    }
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}


function getSelectedText() {
    var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
    }
    // console.log(text);
    return text;
}

function addSelectedText() {
    var def_text = document.getElementById("definition_id");
    var link_text = document.getElementById("link_id");
    def_text.value = "";
    link_text.value = "";

    var text = getSelectedText();
    temp_term = text;
    document.getElementById("modal_title_id").innerHTML = "Add Term: " + text;
}

function editSelectedText() {
    var def_text = document.getElementById("definition_id");
    var link_text = document.getElementById("link_id");
    def_text.value = "";
    link_text.value = "";

    var text = getSelectedText();
    temp_term = text;

    // if (data[text] == null) {
    //     // need to close with error
    //     console.log("no term found");
    //     return;
    // }
    console.log(data);

    document.getElementById("modal_title_id").innerHTML = "Edit Term: " + text;
}







// print_terms();
console.log(data);

if (typeof(window) !== 'undefined') {
  window.addEventListener("contextmenu", function (event) {
    event.preventDefault();
    var contextElement = document.getElementById("context-menu");
    contextElement.style.top = event.offsetY + "px";
    contextElement.style.left = event.offsetX + "px";
    contextElement.classList.add("active");
  });

  window.addEventListener("click", function () {
    document.getElementById("context-menu").classList.remove("active");
  });
}





//Function: Highlights given words in a html file
jQuery.fn.highlight = function (pat) {
  console.log("ran")
  function innerHighlight(node, pat) {
    var skip = 0;
    if (node.nodeType == 3) {
      var pos = node.data.toUpperCase().indexOf(pat);
      pos -= (node.data.substr(0, pos).toUpperCase().length - node.data.substr(0, pos).length);
      if (pos >= 0) {
        var spannode = document.createElement('span');
        spannode.className = 'highlight';
        var middlebit = node.splitText(pos);
        var endbit = middlebit.splitText(pat.length);
        var middleclone = middlebit.cloneNode(true);
        spannode.appendChild(middleclone);
        middlebit.parentNode.replaceChild(spannode, middlebit);
        skip = 1;
      }
    }
    else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
      for (var i = 0; i < node.childNodes.length; ++i) {
        i += innerHighlight(node.childNodes[i], pat);
      }
    }
    return skip;
  }
  return this.length && pat && pat.length ? this.each(function () {
    innerHighlight(this, pat.toUpperCase());
  }) : this;
}; // End highlight function

//Function: removeHighlight removes the highlight css from terms
jQuery.fn.removeHighlight = function () {
  return this.find("span.highlight").each(function () {
    this.parentNode.firstChild.nodeName;
    with (this.parentNode) {
      replaceChild(this.firstChild, this);
      normalize();
    }
  }).end();
}; // End removeHighlight function

// Function: highlightText highlights any word in the HTML that matches wordString
function highlightText(wordString) {
  $('body').highlight(wordString);
} // End Function: highlightText

// Function: unhighlightText removes highlight from any word in the HTML that matches wordString
function UnhighlightText(wordString) {
  $('body').removeHighlight(wordString);
} // End Function: unhighlightText

// Function: highlightDefinedTerms highlights all defined terms in the json file
function highlightDefinedTerms() {
  var definedTerms = print_terms(); //Get list of defined terms
  for (var i = 0; i < definedTerms.length; i++) {
    highlightText(definedTerms[i]);
  }
} // End Function: highlightDefinedTerms

// Function: UnhighlightDefinedTerms removes highlight from all defined terms in the json file
function UnhighlightDefinedTerms() {
  var definedTerms = print_terms(); //Get list of defined terms
  for (var i = 0; i < definedTerms.length; i++) {
    UnhighlightText(definedTerms[i]);
  }
} // End Function: UnhighlightDefinedTerms





////////////////////////////
///SERVER.JS///////////////
//////////////////////////

/***********************
  Load Components!
  Express      - A Node.js Framework
  Body-Parser  - A tool to help use parse the data in a post request
  Pg-Promise   - A database tool to help use connect to our PostgreSQL database
***********************/
var express = require('express'); //Ensure our express framework has been added
var app = express();
var bodyParser = require('body-parser'); //Ensure our body-parser tool has been added
app.use(bodyParser.json());              // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

//Create Database Connection
var pgp = require('pg-promise')();

/**********************
  Database Connection information
  host: This defines the ip address of the server hosting our database.  We'll be using localhost and run our database on our local machine (i.e. can't be access via the Internet)
  port: This defines what port we can expect to communicate to our database.  We'll use 5432 to talk with PostgreSQL
  database: This is the name of our specific database.  From our previous lab, we created the football_db database, which holds our football data tables
  user: This should be left as postgres, the default user account created when PostgreSQL was installed
  password: This the password for accessing the database.  You'll need to set a password USING THE PSQL TERMINAL THIS IS NOT A PASSWORD FOR POSTGRES USER ACCOUNT IN LINUX!
**********************/
const dbConfig = {
  host: 'localhost',
  port: 1234,
  database: 'definitions_db',
  user: 'postgres',
  password: 'postgres'
};

var db = pgp(dbConfig);

// set the view engine to ejs
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/'));//This line is necessary for us to use relative paths and access our resources directory



app.get('/', function(req, res) {
  res.render('test_site',{
    my_title:"Test Page"
  });
});



app.listen(3000);
console.log('3000 is the magic port');