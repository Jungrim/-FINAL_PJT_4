window.onload = function() {
    drawMap('#container'); // id로 불러오기
};

//지도 그리기
function drawMap(target) {
    // const center = d3.geoCentroid(geojson); // 지도 중심
    // 캔버스 설정
    var width = 2000;
    var height = 400;
    
    var initialScale = 5500;
    var initialX = -11200; //초기 위치값 X
    var initialY = 4080; //초기 위치값 Y
    var labels;

    // 투사법 설정
    var projection = d3.geo
        .mercator()
        .scale(initialScale)
        .translate([initialX, initialY]);

    // 지도 path
    var path = d3.geo.path()
        .projection(projection);

    //줌
    var zoom = d3.behavior.zoom()
        .translate(projection.translate())
        .scale(projection.scale())
        .scaleExtent([height, 800 * height])
        .on('zoom', zoom);

    // 지도를 그릴 svg 설정
    var svg = d3.select(target)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('id', 'map')
        .attr('class', 'map');

    var states = svg.append('g')
        .attr('id', 'states')
        .call(zoom);

    states.append('rect')
        .attr('class', 'background')
        .attr('width', width)
        .attr('height', height);

    //geoJson데이터를 파싱하여 지도그리기
    d3.json('../json/dong.json', function(json) {
        states.selectAll('path') //지역 설정
            .data(json.features)
            .enter()
            .append('path')
            .attr('d', path)
            .attr('id', function(d) {
                return 'path-' + d.properties.sidonm;
            });

        labels = states
            .selectAll('text')
            .data(json.features) //라벨표시
            .enter()
            .append('text')
            .attr('transform', translateTolabel)
            .attr('id', function(d) {
                return 'label-' + d.properties.sidonm;
            })
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .text(function(d) {
                return d.properties.adm_nm; // 동 이름 표시
            });
    });

    //텍스트 위치 조절 - 하드코딩으로 위치 조절을 했습니다.
    function translateTolabel(d) {
        var arr = path.centroid(d);
        if (d.properties.code == 31) {
            //서울 경기도 이름 겹쳐서 경기도 내리기
            arr[1] +=
                d3.event && d3.event.scale
                    ? d3.event.scale / height + 20
                    : initialScale / height + 20;
        } else if (d.properties.code == 34) {
            //충남은 조금 더 내리기
            arr[1] +=
                d3.event && d3.event.scale
                    ? d3.event.scale / height + 10
                    : initialScale / height + 10;
        }
        return 'translate(' + arr + ')';
    }

    function zoom() {
        projection.translate(d3.event.translate).scale(d3.event.scale);
        states.selectAll('path').attr('d', path);
        labels.attr('transform', translateTolabel);
    }
}
