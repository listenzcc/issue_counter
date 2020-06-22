class TimeLine {
  constructor(svg) {
    this.name = "TimeLine";
    this.svg = svg;

    var height = parseFloat(svg.style("height").replace("px", ""));
    var width = parseFloat(svg.style("width").replace("px", ""));

    this.left = 0 + 5;
    this.right = width + 5;
    this.y = height / 2;
  }

  rescale(num, start, end) {
    this.num = num;
    this.start = start;
    this.end = end;
  }

  map(a, a1, a2, b1, b2) {
    var r = (a - a1) / (a2 - a1);
    return b1 + (b2 - b1) * r;
  }

  ticks() {
    this.svg.selectAll("*").remove();

    this.svg
      .append("line")
      .attr("x1", this.left)
      .attr("x2", this.right)
      .attr("y1", this.y)
      .attr("y2", this.y)
      .style("stroke", "rgba(29, 57, 184, 0.9)");

    var x = 0;
    var y1 = this.y;
    var y2 = this.y - 10;
    for (let i = 0; i < this.num; i++) {
      x = this.map(i, 0, this.num, this.left, this.right);
      this.svg
        .append("line")
        .attr("x1", x)
        .attr("x2", x)
        .attr("y1", y1)
        .attr("y2", y2)
        .style("stroke", "rgba(29, 57, 184, 0.9)");
    }
  }
}

function ruling_canvas(start, end) {
  var svg = d3.select("#Canvas");
  console.log(svg);

  var width = svg.style("width");
  var height = svg.style("height");
  console.log(width, height);

  var timeline = new TimeLine(svg);
  timeline.rescale(10, 0, 100);
  timeline.ticks();
}
