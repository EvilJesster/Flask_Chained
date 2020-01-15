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
    // don't do anything if the number is permanent
    if (td.children().length == 1)
        return;

    let to_toggle = $(td.children()[1]);
    let pencilmarks = $(td.children()[0]);

    if (to_toggle.hasClass("permanent")) return;

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

// loads preset numbers
load_preset_numbers = (id, nums) => {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (nums[i * 9 + j] != "0") {
                let to_show = $(get_td(id, j, i).children()[1]);
                let pencilmarks = $(get_td(id, j, i).children()[0]);
                to_show.show();
                pencilmarks.remove();
                to_show.addClass("permanent");
                to_show.text(nums[i * 9 + j]);
            }
        }
    }
};

// pulls board state
get_board_state = (id) => {
    let res = "";

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            let td = get_td(id, j, i);
            let t = "";
            if (td.children().length == 1) {
                t = $(td.children()[0]).text();
            } else {
                t = $(td.children()[1]).text();
            }
            res += (t == "" ? "0" : t);
        }
    }

    return res;
};

// check if board is correct
check_board_correct = (id, uuid) => {
    let state = get_board_state(id);

    $.get("/api/check_answer/" + uuid + "/" + state, {}, (data, status) => {
        data = JSON.parse(data);
        if (data) {
            alert("Board is correct! Congrats!");
            window.location = "/user/home";
        } else {
            alert("Board is incorrect..");
        }
    });

};

// get user number state
get_user_number_state = (id) => {
    let ret = "";

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            let cur_td = get_td(id, j, i);
            if (cur_td.children().length == 2 && $(cur_td.children()[1]).text() != "") {
                // meaning this cell is user-modifiable
                ret += $(cur_td.children()[1]).text();
            } else {
                // otherwise
                ret += "_";
            }
        };
    };

    return ret;
};

// get user pencilmark state
get_user_pencilmark_state = (id) => {
    let ret = "";

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            let cur_td = get_td(id, j, i);
            if (cur_td.children().length == 2) {
                let child = $(cur_td.children()[0]).children();

                for (let k = 0; k < 9; k++) {
                    ret += ($(child[k]).css("display") == "none" ? "_" : $(child[k]).text());
                }

            } else {
                ret += "_________";
            }
        };
    };

    return ret;
};

// save board state (talks to server)
save_board_state = (id, uuid) => {
    // get board states
    let cur_num_state = get_user_number_state('#puzzle');
    let cur_pencilmark_state = get_user_pencilmark_state('#puzzle');

    $.post("/api/save_state/" + uuid, {
        numbers: cur_num_state,
        pencilmarks: cur_pencilmark_state
    }, () => {});
};

recover_save_state = (id, numbers, pencilmarks) => {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            // set number
            if (numbers[i * 9 + j] !== "_") {
                toggle_number(get_td(id, j, i), numbers[i * 9 + j]);
            }
            for (let k = 0; k < 9; k++) {
                if (pencilmarks[i * 91 + j * 8 + k] != "_") {
                    toggle_pencilmark(get_td(id, i, j),
                        parseInt(pencilmarks[i * 91 + j * 8 + k]));
                }
            }
        };
    };
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