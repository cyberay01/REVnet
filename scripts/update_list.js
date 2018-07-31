let last_refresh = new Date();

function new_element(tag_name, attributes, children=[]){
  el = document.createElement(tag_name);
  for (let attr in attributes){
    el.setAttribute(attr, attributes[attr]);
  }
  for (let child in children){
    el.appendChild(children[child]);
  }
  return el;
}

function insert_meme(desc){
  let new_li = new_element('div', {'class': 'location'}, [
    new_element('text', {'class': 'host_name'}, [document.createTextNode(desc['host_name'])]),
    new_element('br'),
    new_element('text', {'class': 'address'}, [document.createTextNode(desc['address'])]),
    new_element('br'),
    new_element('text', {'class': 'comment'}, [document.createTextNode(desc['comment'])]),
    new_element('br'),
    new_element('br')
  ]);
  let container = document.querySelector("#loc_list");
  container.insertBefore(new_li, container.children[0]);
}

function refresh_memes() {
  fetch('/updated_list?since=' + last_refresh.getTime()/1000, {'credentials': 'include'} )
    .then((data) => {return data.json();})
    .then((json) => {
      for (let i in json) {
        insert_meme(json[i]);
      }
    });
  last_refresh = new Date();
}


setInterval(refresh_memes, 3000);
