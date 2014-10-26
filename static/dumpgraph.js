$('#submitBtn').click( function(event){
  event.preventDefault();
  username = $('input#username').val();
  $("#dumpgraph").html('Loading '+username+'...');
  //follow = $("input[name=follow]:checked").val();
  dumpgraph('/gather/bb?username='+username);
  //dumpgraph('/gather/f?username='+username);
  $('input#username').val('');
});
// "/actions/json"
function dumpgraph(linkpile) {

var width = 960,
    height = 500

var svg = d3.select("#dumpgraph").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(.01)
    .distance(100)
    .charge(-100)
    .size([width, height]);

d3.json(linkpile, function(error, json) {
  try {
    update(json);
  } catch(err) {
      $("#dumpgraph").html('User not found. Or they have no friends. Usernames are case-sensitive.');
  }
});

function update(root) {
  console.log(root);
  root.nodes[root.centerindex].fixed = true;
  root.nodes[root.centerindex].x = width/2;
  root.nodes[root.centerindex].y = height=2;
  force
      .nodes(root.nodes)
      .links(root.links)
      .start();

  var link = svg.selectAll(".link")
      .data(root.links)
    .enter().append("line")
      .attr("class", "link");

  var node = svg.selectAll(".node")
      .data(root.nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .on("click",click)
      .call(force.drag);

  node.append("image")
      .attr("xlink:href", "http://www.producthunt.com/favicon.ico")
      .attr("x", -8)
      .attr("y", -8)
      .attr("width", 16)
      .attr("height", 16);

  node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
}
}
function click(d) {
  if (d3.event.defaultPrevented) return; // ignore drag
  console.log(d.name);
  $("#dumpgraph").html('Loading '+d.name+'...');
  dumpgraph('/gather/bb?username='+d.name);
}
