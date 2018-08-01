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
  let new_div = new_element('div', {'class': 'location'}, [
    new_element('text', {'class': 'host_name'}, [document.createTextNode('Name of Place: ' + desc['host_name'])]),
    new_element('br'),
    new_element('text', {'class': 'address'}, [document.createTextNode('Address: ' + desc['address'])]),
    new_element('br'),
    new_element('text', {'class': 'comment'}, [document.createTextNode('Comment: ' + desc['comment'])]),
    new_element('br'),
    new_element('br')
  ]);
  let container = document.querySelector("#loc_list");
  container.insertBefore(new_div, container.children[0]);
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