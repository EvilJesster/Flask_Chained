initialize_board = (id) => {
    let board = $(id);
    let full_html = "";
    full_html += "<table>";
    for (let i = 0; i < 9; i++) {
        full_html += "<tr>";
        for (let j = 0; j < 9; j++) {
            full_html += "<td><div class='pencil-marks'><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></div>     <div class='actual-number'>1</div></td>";
        }
        full_html += "</tr>";
    }

    full_html += "</table>";


    board.html(full_html);

};