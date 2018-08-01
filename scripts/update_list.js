// update new locations without user having to reload the page
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

function insert_location(desc){
  let new_div = new_element('p', {'id': 'box', 'class': 'location'}, [
    new_element('text', {'id': 'place', 'class': 'host_name'}, [document.createTextNode(desc['host_name'])]),
    new_element('br'),
    new_element('text', {'id': 'address', 'class': 'address'}, [document.createTextNode('Address: ' + desc['address'])]),
    new_element('br'),
    new_element('text', {'id': 'type','class': 'comment'}, [document.createTextNode('Comment: ' + desc['comment'])]),
    new_element('br'),
  ]);
  let container = document.querySelector("#loc_list");
  container.insertBefore(new_div, container.children[1]);
}

function clearBox(elementID)
{
    document.getElementById(elementID).innerHTML = "";
}

function refresh_locations(lng, lat) {
  fetch("/updated_list?lng=" + lng + "&lat=" + lat, {'credentials': 'include'} )
    .then((data) => {return data.json();})
    .then((json) => {
      for (let i in json) {
        insert_location(json[i]);
      }
    });
  last_refresh = new Date();
}