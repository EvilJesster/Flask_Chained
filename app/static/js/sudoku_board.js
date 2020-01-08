window.cur_td = null;
window.SHIFT = false;

initialize_board = (id) => {
    let board = $(id);
    let full_html = "";
    full_html += "<table>";
    for (let i = 0; i < 9; i++) {
        full_html += "<tr>";
        for (let j = 0; j < 9; j++) {
            full_html += "<td><div class='pencil-marks'><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></div>     <div class='actual-number'></div></td>";
        }
        full_html += "</tr>";
    }

    full_html += "</table>";


    board.html(full_html);

    // link events to all the <td>s. Each individiaul <td> is a square in the board that we can hover over on
    let all_tds = $(id + " td");

    if (all_tds.length != 81) {
        alert("Something is wrong with board generation!");
        return;
    }

    for (let i = 0; i < 81; i++) {
        let cur_td = $(all_tds[i]);
        let cur_pencilmarks = $(cur_td.children()[0]).children();
        let cur_actualnumber = $(cur_td.children()[1]);

        // hide all numbers
        cur_actualnumber.hide();
        // hide all pencilmarks
        for (let j = 0; j < 9; j++) {
            $(cur_pencilmarks[j]).hide();
        }

        cur_td.hover(() => {
            window.cur_td = $(cur_td);
        });


    }

};

get_td = (id, row, col) => {
    return $($(id + " td")[col * 9 + row]);
};

toggle_pencilmark = (td, number) => {
    $($(td.children()[0]).children()[number - 1]).toggle();
};

toggle_number = (td, number) => {
    let to_toggle = $(td.children()[1]);
    let pencilmarks = $(td.children()[0]);

    if (to_toggle.text() == "") {
        to_toggle.text(number);
        to_toggle.show();
        pencilmarks.hide();
    } else if (to_toggle.text() == number) {
        to_toggle.text("");
        to_toggle.hide();
        pencilmarks.show();
    } else {
        to_toggle.text(number);
        pencilmarks.hide();
    }

};

// shows pencilmark for number in td on (row, col)
show_pencilmark = (id, row, col, number) => {
    if (number < 1 || number > 9) {
        alert("Invalid pencilmark number");
        return;
    }

    let the_td = get_td(id, row, col);
    console.log(the_td);

    toggle_pencilmark(the_td, number);

};

$(document).ready(() => {
    document.onkeydown = (e) => {
        if (e.keyCode == 16) {
            window.SHIFT = true;
        }
        if (e.which >= 49 && e.which <= 57) {
            if (window.SHIFT) {
                toggle_pencilmark(window.cur_td, e.which - 48);
            } else {
                toggle_number(window.cur_td, e.which - 48);
            }
        }
    };

    document.onkeyup = (e) => {
        if (e.keyCode == 16) {
            window.SHIFT = false;
        }
    };

});