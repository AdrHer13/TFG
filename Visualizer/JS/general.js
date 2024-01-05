let game_obj = {};
let round_obj = {};
let turn_obj = {};
let phase_obj = {};

let gameDirection = 'forward'; // or "backward"


function init_events() {
    let input = jQuery('#get_file');
    let load_game = jQuery('#load_game');
    load_game.on('click', function (e) {
        input.click();
    })

    input.on('click', function (e) {
        input.val('')

        // resetear el tablero
        jQuery('.node').add('.road').add('.vertical_road').css('background', 'none').css('border', 'none').text('');
        $('#contador_rondas').val('').change();
        $('#contador_turnos').val('').change();
        $('#contador_fases').val('').change();
    })

    input.on('change', function (e) {
        let file = document.getElementById("get_file").files[0];
        if (file) {
            let reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (evt) {
                game_obj = JSON.parse(evt.target.result);

                init_events_with_game_obj();
                addLogFromJSON();
                setup();
            }
            reader.onerror = function (evt) {
                console.log('Error al cargar el archivo');
            }
        }

        for (let i = 1; i < 5; i++) {
            let textarea = $('#buildings_P' + i);
            textarea.text('');
        }
        game_obj = {};
        round_obj = {};
        turn_obj = {};
        phase_obj = {};


        jQuery('#puntos_victoria_J1').text(0);
        jQuery('#puntos_victoria_J2').text(0);
        jQuery('#puntos_victoria_J3').text(0);
        jQuery('#puntos_victoria_J4').text(0);
    });


    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
}

function addLogFromJSON() {
    $('#contador_rondas').val(1).change()
    $('#contador_turnos').val(1).change()
    $('#contador_fases').val(1).change()

    $('#rondas_maximas').text(Object.keys(game_obj['game']).length)
}

function addSetupBuildings() {
    setup_obj = game_obj['setup'];

    for (let i = 0; i < 4; i++) {
        let textarea = $('#buildings_P' + (i + 1))
        for (let j = 0; j < setup_obj['P' + i].length; j++) {
            let node = jQuery('#node_' + setup_obj['P' + i][j]['id']);
            let road = '';
            if (setup_obj['P' + i][j]['id'] < setup_obj['P' + i][j]['road']) {
                road = jQuery('#road_' + setup_obj['P' + i][j]['id'] + '_' + setup_obj['P' + i][j]['road']);
            } else {
                road = jQuery('#road_' + setup_obj['P' + i][j]['road'] + '_' + setup_obj['P' + i][j]['id']);
            }

            let str = 'node: ' + setup_obj['P' + i][j]['id'] + ' | ' + 'type: ' + 'T' + '\r\n';
            str += 'node: ' + setup_obj['P' + i][j]['id'] + ' | ' + 'road_to: ' + setup_obj['P' + i][j]['road'] + ' | ' + 'type: ' + 'R' + '\r\n';

            textarea.text(textarea.text() + str);

            paint_it_player_color(i, node);
            paint_it_player_color(i, road);

            node.html('<i class="fa-solid fa-house"></i>');
        }
    }
}

function terrainSetup() {
    terrain = game_obj['setup']['board']['board_terrain'];

    for (let i = 0; i < terrain.length; i++) {
        let terrain_div = jQuery('#terrain_' + i);
        let terrain_number = jQuery('#terrain_' + i + ' .terrain_number');

        html = '';
        if (terrain[i]['probability'] != 0) {
            if (terrain[i]['probability'] == 6 || terrain[i]['probability'] == 8) {
                html += '<span style="color: red;">';
            } else {
                html += '<span>';
            }
            html += terrain[i]['probability'] + '</span>';
        } else {
            html += '<i class="fa-solid fa-user-ninja fa-2x" data-toggle="tooltip" data-placement="top" title="Ladrón"></i>'
        }

        terrain_number.html(html);
        terrain_div.removeClass(['terrain_cereal', 'terrain_mineral', 'terrain_clay', 'terrain_wood', 'terrain_wool', 'terrain_desert'])
        terrain_div.addClass(getTerrainTypeClass(terrain[i]['terrain_type']));
        //                terrain_div.text(terrain_div.text() + '');
    }
}

function nodeSetup() {
    nodes = game_obj['setup']['board']['board_nodes'];

    for (let i = 0; i < nodes.length; i++) {
        let node = jQuery('#node_' + i);

        // TODO: Añadir icono de puerto a las costeras O añadir un icono en el mar
        node.html(fromHarborNumberToMaterials(nodes[i]['harbor']));
    }
}

function fromHarborNumberToMaterials(harborNumber) {
    switch (harborNumber) {
        case 0:
            return '<i class="fa-solid fa-wheat-awn"></i><span>2:1</span>';
        case 1:
            return '<i class="fa-solid fa-mountain-sun"></i><span>2:1</span>';
        case 2:
            return '<i class="fa-solid fa-trowel-bricks"></i><span>2:1</span>';
        case 3:
            return '<i class="fa-solid fa-wand-sparkles"></i><span>2:1</span>';
        case 4:
            return '<i class="fa-brands fa-cotton-bureau"></i><span>2:1</span>';
        case 5:
            return '<span>3:1</span>'
        case -1:
            return '';
        default:
            //            alert('Caso ilegal de terreno');
            break;
    }
}

function getTerrainTypeClass(terrainType) {
    switch (terrainType) {
        case 0:
            return 'terrain_cereal';
        case 1:
            return 'terrain_mineral';
        case 2:
            return 'terrain_clay';
        case 3:
            return 'terrain_wood';
        case 4:
            return 'terrain_wool';
        case -1:
            return 'terrain_desert';
        default:
            //            alert('Caso ilegal de terreno');
            break;
    }
}

function init_events_with_game_obj() {
    let contador_rondas = jQuery('#contador_rondas');
    let contador_turnos = jQuery('#contador_turnos');
    let contador_fases = jQuery('#contador_fases');

    let ronda_previa_btn = jQuery('#ronda_previa_btn');
    let ronda_siguiente_btn = jQuery('#ronda_siguiente_btn');

    let turno_previo_btn = jQuery('#turno_previo_btn');
    let turno_siguiente_btn = jQuery('#turno_siguiente_btn');

    let fase_previa_btn = jQuery('#fase_previa_btn');
    let fase_siguiente_btn = jQuery('#fase_siguiente_btn');

    let millis_for_play = jQuery('#millis_for_play');
    let play_btn = jQuery('#play_btn');
    let playIntervalNumber = 0;

    contador_rondas.off().on('change', function (e) {
        if (contador_rondas.val() === '') {
            return;
        }

        if (parseInt(contador_rondas.val()) < 1) {
            contador_rondas.val(1).change();
        }
        if (parseInt(contador_rondas.val()) > Object.keys(game_obj['game']).length) {
            contador_rondas.val(Object.keys(game_obj['game']).length).change();

            play_btn.click()
        }

        jQuery('#actual_round').text(contador_rondas.val())

        round_obj = game_obj['game']['round_' + (contador_rondas.val() - 1)];
        contador_turnos.val(1).change();
    });
    contador_turnos.off().on('change', function (e) {
        if (contador_turnos.val() === '') {
            return;
        }

        let actual_player_json = parseInt(contador_turnos.val()) - 1; // 0 - 3

        if (parseInt(contador_turnos.val()) > 4) {
            contador_rondas.val(parseInt(contador_rondas.val()) + 1).change()
            contador_turnos.val(1).change()
            return;
        }
        if (parseInt(contador_turnos.val()) < 1) {
            if (parseInt(contador_rondas.val()) < 1) {
                contador_turnos.val(1).change();
            } else {
                contador_rondas.val(parseInt(contador_rondas.val()) - 1).change();
                contador_turnos.val(4).change();
            }
            return;
        }

        deleteCaretStyling();

        $('#P0').css('border', '5px solid lightcoral');
        $('#P1').css('border', '5px solid lightblue');
        $('#P2').css('border', '5px solid lightgreen');
        $('#P3').css('border', '5px solid lightyellow');

        let border_colors = ['red', 'blue', 'green', 'yellow'];
        $('#P' + actual_player_json).css('border', '5px solid ' + border_colors[actual_player_json]);

        turn_obj = round_obj['turn_P' + actual_player_json];
        //contador_fases.val(1).change();
    });
    contador_fases.off().on('change', function (e) {
        if (contador_fases.val() === '') {
            return;
        }
        let actual_player_json = parseInt(contador_turnos.val()) - 1; // 0 - 3

        if (parseInt(contador_fases.val()) > 4) {
            contador_turnos.val(parseInt(contador_turnos.val()) + 1).change();
            contador_fases.val(1).change();
            return;
        }

        if (parseInt(contador_fases.val()) < 1) {
            contador_turnos.val(parseInt(contador_turnos.val()) - 1).change();
            contador_fases.val(4).change();
            return;
        }

        let commerce_log_text = jQuery('#commerce_log_text');
        let other_useful_info_text = jQuery('#other_useful_info_text');
        let cereal_quantity_text = parseInt($('#hand_P' + actual_player_json + ' .cereal_quantity').text());
        let mineral_quantity_text = parseInt($('#hand_P' + actual_player_json + ' .mineral_quantity').text());
        let clay_quantity_text = parseInt($('#hand_P' + actual_player_json + ' .clay_quantity').text());
        let wood_quantity_text = parseInt($('#hand_P' + actual_player_json + ' .wood_quantity').text());
        let wool_quantity_text = parseInt($('#hand_P' + actual_player_json + ' .wool_quantity').text());
        let diceroll_div = jQuery('#diceroll');
        let html = '';

        other_useful_info_text.empty();
        switch (parseInt(contador_fases.val()) - 1) {
            case 0:
                phase_obj = turn_obj['start_turn'];

                commerce_log_text.empty();
                for (let i = 0; i < 4; i++) {
                    changeHandObject(i, phase_obj['hand_P' + i]);
                }

                if (gameDirection === 'forward') {
                    diceroll_div.text('Diceroll: ' + phase_obj['dice']);

                    if (phase_obj['dice'] == 7) {
                        // jQuery('#terrain_' + phase_obj['past_thief_terrain']).text('')
                        if (game_obj['setup']['board']['board_terrain'][phase_obj['past_thief_terrain']]['probability'] != 0) {
                            jQuery('#terrain_' + phase_obj['past_thief_terrain'] + ' .terrain_number').html('<span>' + game_obj['setup']['board']['board_terrain'][phase_obj['past_thief_terrain']]['probability'] + '</span>');
                        } else {
                            jQuery('#terrain_' + phase_obj['past_thief_terrain'] + ' .terrain_number').html('')
                        }

                        jQuery('#terrain_' + phase_obj['thief_terrain'] + ' .terrain_number').html('<i class="fa-solid fa-user-ninja fa-2x" data-toggle="tooltip" data-placement="top" title="Ladrón"></i>');
                    }

                    if (phase_obj['development_card_played'] && phase_obj['development_card_played'].length) {
                        // console.log('SE JUEGA CARTA DE DESAROLLO AL INICIO DEL TURNO' + '| Ronda: ' + contador_rondas.val() + ' Turno: ' + contador_turnos.val())
                        on_development_card_played(phase_obj['development_card_played'][0])
                    }
                } else if (gameDirection === 'backward') {
                    phase_obj = turn_obj['commerce_phase'];
                    deleteCaretStyling();

                    for (let i = 0; i < phase_obj.length; i++) {
                        if (phase_obj[i]['trade_offer'] == 'played_card') {
                            off_development_card_played(phase_obj[i]['development_card_played'])
                        }
                    }
                }
                break;
            case 1:
                phase_obj = turn_obj['commerce_phase'];
                commerce_log_text.empty();

                for (let i = 0; i < phase_obj.length; i++) {

                    if (phase_obj[i]['trade_offer'] == 'None') {
                        // break, porque debería de ser el último de todas maneras

                        // si no hay ningún comercio que ponga PJ: No trade
                        if (phase_obj.length == 1) {
                            html += '<div class="offer"><p>';
                            html += '<span class="commerce_P' + contador_turnos.val() + '">P' + contador_turnos.val() + '</span>: No trade';
                            html += '<p></div>'
                            html += '<hr/>'
                        }

                        break;
                    }
                    if (phase_obj[i]['inviable']) {
                        html += '<div class="offer"><p>';
                        html += '<span class="commerce_P' + contador_turnos.val() + '">P' + contador_turnos.val() + '</span>: Inviable trade';
                        html += '<p></div>'
                        html += '<hr/>'
                        // break, porque no se puede completar el comercio
                        break;
                    }
                    if (phase_obj[i]['harbor_trade']) {
                        let material_chosen_array = ['cereal', 'mineral', 'clay', 'wood', 'wool'];
                        let material_given = material_chosen_array[phase_obj[i]['trade_offer']['gives']];
                        let material_received = material_chosen_array[phase_obj[i]['trade_offer']['receives']];

                        html += '<div class="offer"><p>';
                        html += '<span class="commerce_P' + contador_turnos.val() + '">P' + contador_turnos.val() + '</span>: Harbor trade';
                        html += '<br><span class="gives">Gives: ';
                        html += material_given.charAt(0).toUpperCase() + material_given.slice(1);
                        jQuery('#hand_P' + actual_player_json + ' .' + material_given).removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                        jQuery('#hand_P' + actual_player_json + ' .' + material_given + ' .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');

                        html += '</span>';
                        html += '<br><span class="receives">Receives: ';

                        html += material_received.charAt(0).toUpperCase() + material_received.slice(1);
                        jQuery('#hand_P' + actual_player_json + ' .' + material_received).removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                        jQuery('#hand_P' + actual_player_json + ' .' + material_received + ' .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');

                        html += '</span>';
                        html += '</p></div>';
                        html += '<hr/>';

                        // se actualiza la mano del jugador si avanza, se ignora si va hacia atrás
                        if (gameDirection === 'forward') {
                            changeHandObject(actual_player_json, phase_obj[i]['answer'])
                        }

                    } else if (phase_obj[i]['trade_offer'] == 'played_card') {
                        // Se ha jugado una carta de desarrollo

                        html += '<div><p>';
                        html += '<span class="commerce_P' + contador_turnos.val() + '">P' + contador_turnos.val() + '</span>: Played a development card';
                        html += '</p></div>';

                        if (gameDirection === 'forward') {
                            on_development_card_played(phase_obj[i]['development_card_played']);
                        }
                    } else {
                        html += '<div class="offer"><p>';
                        html += '<span class="commerce_P' + contador_turnos.val() + '">P' + contador_turnos.val() + '</span>: Offer';
                        html += '<br><span class="gives">';
                        html += 'Gives: ' + 'Cereal: ' + phase_obj[i]['trade_offer']['gives']['cereal'] + ' | ';
                        html += 'Mineral: ' + phase_obj[i]['trade_offer']['gives']['mineral'] + ' | ';
                        html += 'Wool: ' + phase_obj[i]['trade_offer']['gives']['wool'] + ' | ';
                        html += 'Wood: ' + phase_obj[i]['trade_offer']['gives']['wood'] + ' | ';
                        html += 'Clay: ' + phase_obj[i]['trade_offer']['gives']['clay'] + '</span>';

                        html += '<br><span class="receives">';
                        html += 'Receives: ' + 'Cereal: ' + phase_obj[i]['trade_offer']['receives']['cereal'] + ' | ';
                        html += 'Mineral: ' + phase_obj[i]['trade_offer']['receives']['mineral'] + ' | ';
                        html += 'Wool: ' + phase_obj[i]['trade_offer']['receives']['wool'] + ' | ';
                        html += 'Wood: ' + phase_obj[i]['trade_offer']['receives']['wood'] + ' | ';
                        html += 'Clay: ' + phase_obj[i]['trade_offer']['receives']['clay'] + '</span>';
                        html += '</p></div>';

                        html += '<div class="answers">'
                        for (let j = 0; j < phase_obj[i]['answers'].length; j++) {
                            let counteroffer_counter = 0
                            for (let n = 0; n < phase_obj[i]['answers'][j].length; n++) {
                                html += '<div>';

                                if (phase_obj[i]['answers'][j][n]['count'] == 1) {

                                    if (phase_obj[i]['answers'][j][n]['response'] == true) {
                                        html += '<span class="commerce_P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '"> P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '</span>';
                                        if (phase_obj[i]['answers'][j][n]['completed']) {
                                            html += ': Accepted';

                                            // añadir materiales a mano
                                            let giver_nmbr = phase_obj[i]['answers'][j][n]['giver'];
                                            let receiver_nmbr = phase_obj[i]['answers'][j][n]['receiver'];

                                            let gives_cereal = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['cereal']);
                                            let gives_mineral = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['mineral']);
                                            let gives_clay = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['clay']);
                                            let gives_wood = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wood']);
                                            let gives_wool = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wool']);

                                            let receives_cereal = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['cereal']);
                                            let receives_mineral = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['mineral']);
                                            let receives_clay = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['clay']);
                                            let receives_wood = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wood']);
                                            let receives_wool = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wool']);

                                            if (gameDirection === 'forward') {
                                                changeHandObject(giver_nmbr, {
                                                    'cereal': (parseInt($('#hand_P' + giver_nmbr + ' .cereal_quantity').text()) - gives_cereal + receives_cereal),
                                                    'mineral': (parseInt($('#hand_P' + giver_nmbr + ' .mineral_quantity').text()) - gives_mineral + receives_mineral),
                                                    'clay': (parseInt($('#hand_P' + giver_nmbr + ' .clay_quantity').text()) - gives_clay + receives_clay),
                                                    'wood': (parseInt($('#hand_P' + giver_nmbr + ' .wood_quantity').text()) - gives_wood + receives_wood),
                                                    'wool': (parseInt($('#hand_P' + giver_nmbr + ' .wool_quantity').text()) - gives_wool + receives_wool),
                                                });
                                                changeHandObject(receiver_nmbr, {
                                                    'cereal': (parseInt($('#hand_P' + receiver_nmbr + ' .cereal_quantity').text()) + gives_cereal - receives_cereal),
                                                    'mineral': (parseInt($('#hand_P' + receiver_nmbr + ' .mineral_quantity').text()) + gives_mineral - receives_mineral),
                                                    'clay': (parseInt($('#hand_P' + receiver_nmbr + ' .clay_quantity').text()) + gives_clay - receives_clay),
                                                    'wood': (parseInt($('#hand_P' + receiver_nmbr + ' .wood_quantity').text()) + gives_wood - receives_wood),
                                                    'wool': (parseInt($('#hand_P' + receiver_nmbr + ' .wool_quantity').text()) + gives_wool - receives_wool),
                                                });
                                            }

                                            // añadir caret
                                            if (gives_cereal - receives_cereal < 0) {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_cereal - receives_cereal > 0) {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_mineral - receives_mineral < 0) {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_mineral - receives_mineral > 0) {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_clay - receives_clay < 0) {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_clay - receives_clay > 0) {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_wood - receives_wood < 0) {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_wood - receives_wood > 0) {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_wool - receives_wool < 0) {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_wool - receives_wool > 0) {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }
                                            // fin añadir materiales a mano

                                        } else {
                                            html += ': Accepted | Cannot be completed (lack of materials)';
                                        }
                                    } else {
                                        if (phase_obj[i]['answers'][j][n]['count'] == phase_obj[i]['answers'][j].length) {
                                            html += '<span class="commerce_P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '"> P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '</span>';
                                            html += ': Denied';
                                        }
                                    }
                                } else {
                                    counteroffer_counter++;
                                    // hay contraoferta
                                    html += '<div class="offer"><p>';
                                    html += '<span class="commerce_P' + (phase_obj[i]['answers'][j][n]['giver'] + 1) + '">P' + (phase_obj[i]['answers'][j][n]['giver'] + 1) + '</span>: Counteroffer';
                                    html += '<br><span class="gives">';
                                    html += 'Gives: ' + 'Cereal: ' + phase_obj[i]['answers'][j][n]['trade_offer']['gives']['cereal'] + ' | ';
                                    html += 'Mineral: ' + phase_obj[i]['answers'][j][n]['trade_offer']['gives']['mineral'] + ' | ';
                                    html += 'Wool: ' + phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wool'] + ' | ';
                                    html += 'Wood: ' + phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wood'] + ' | ';
                                    html += 'Clay: ' + phase_obj[i]['answers'][j][n]['trade_offer']['gives']['clay'] + '</span>';

                                    html += '<br><span class="receives">';
                                    html += 'Receives: ' + 'Cereal: ' + phase_obj[i]['answers'][j][n]['trade_offer']['receives']['cereal'] + ' | ';
                                    html += 'Mineral: ' + phase_obj[i]['answers'][j][n]['trade_offer']['receives']['mineral'] + ' | ';
                                    html += 'Wool: ' + phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wool'] + ' | ';
                                    html += 'Wood: ' + phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wood'] + ' | ';
                                    html += 'Clay: ' + phase_obj[i]['answers'][j][n]['trade_offer']['receives']['clay'] + '</span>';
                                    html += '</p></div>';


                                    if (phase_obj[i]['answers'][j][n]['response'] == true) {

                                        html += '<span class="answers commerce_P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '"> P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '</span>';
                                        if (phase_obj[i]['answers'][j][n]['completed']) {
                                            html += ': Accepted';

                                            // añadir materiales a mano
                                            let giver_nmbr = phase_obj[i]['answers'][j][n]['giver'];
                                            let receiver_nmbr = phase_obj[i]['answers'][j][n]['receiver'];

                                            let gives_cereal = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['cereal']);
                                            let gives_mineral = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['mineral']);
                                            let gives_clay = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['clay']);
                                            let gives_wood = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wood']);
                                            let gives_wool = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['gives']['wool']);

                                            let receives_cereal = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['cereal']);
                                            let receives_mineral = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['mineral']);
                                            let receives_clay = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['clay']);
                                            let receives_wood = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wood']);
                                            let receives_wool = parseInt(phase_obj[i]['answers'][j][n]['trade_offer']['receives']['wool']);


                                            if (gameDirection === 'forward') {
                                                changeHandObject(giver_nmbr, {
                                                    'cereal': (parseInt($('#hand_P' + giver_nmbr + ' .cereal_quantity').text()) - gives_cereal + receives_cereal),
                                                    'mineral': (parseInt($('#hand_P' + giver_nmbr + ' .mineral_quantity').text()) - gives_mineral + receives_mineral),
                                                    'clay': (parseInt($('#hand_P' + giver_nmbr + ' .clay_quantity').text()) - gives_clay + receives_clay),
                                                    'wood': (parseInt($('#hand_P' + giver_nmbr + ' .wood_quantity').text()) - gives_wood + receives_wood),
                                                    'wool': (parseInt($('#hand_P' + giver_nmbr + ' .wool_quantity').text()) - gives_wool + receives_wool),
                                                });
                                                changeHandObject(receiver_nmbr, {
                                                    'cereal': (parseInt($('#hand_P' + receiver_nmbr + ' .cereal_quantity').text()) + gives_cereal - receives_cereal),
                                                    'mineral': (parseInt($('#hand_P' + receiver_nmbr + ' .mineral_quantity').text()) + gives_mineral - receives_mineral),
                                                    'clay': (parseInt($('#hand_P' + receiver_nmbr + ' .clay_quantity').text()) + gives_clay - receives_clay),
                                                    'wood': (parseInt($('#hand_P' + receiver_nmbr + ' .wood_quantity').text()) + gives_wood - receives_wood),
                                                    'wool': (parseInt($('#hand_P' + receiver_nmbr + ' .wool_quantity').text()) + gives_wool - receives_wool),
                                                });
                                            }

                                            // añadir caret
                                            if (gives_cereal - receives_cereal < 0) {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_cereal - receives_cereal > 0) {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .cereal .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .cereal').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_mineral - receives_mineral < 0) {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_mineral - receives_mineral > 0) {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .mineral .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .mineral').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_clay - receives_clay < 0) {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_clay - receives_clay > 0) {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .clay .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .clay').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_wood - receives_wood < 0) {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_wood - receives_wood > 0) {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .wood .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .wood').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }

                                            if (gives_wool - receives_wool < 0) {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down');
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased');
                                            } else if (gives_wool - receives_wool > 0) {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up');
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('increased');
                                            } else {
                                                $('#hand_P' + giver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + giver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                                $('#hand_P' + receiver_nmbr + ' .wool .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-minus')
                                                $('#hand_P' + receiver_nmbr + ' .wool').removeClass(['increased', 'neutral', 'decreased']).addClass('neutral')
                                            }
                                            // fin añadir materiales a mano

                                        } else {
                                            html += ': Accepted | Cannot be completed (lack of materials)';
                                        }
                                        // cerramos todos los divs de contraoferta
                                        for (let m = 0; m < counteroffer_counter; m++) {
                                            html += '</div>'
                                        }

                                    } else {
                                        if (phase_obj[i]['answers'][j][n]['count'] == phase_obj[i]['answers'][j].length) {
                                            // se niega la oferta
                                            html += '<span class="answers commerce_P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '"> P' + (parseInt(phase_obj[i]['answers'][j][n]['receiver']) + 1) + '</span>';
                                            html += ': Denied';
                                            // cerramos todos los divs de contraoferta
                                            for (let m = 0; m < counteroffer_counter; m++) {
                                                html += '</div>'
                                            }
                                        } else {
                                            // se niega la oferta pero se ofrece contraoferta (se comprueba viendo si la cuenta es la misma que la longitud del array)
                                            counteroffer_counter++;
                                            html += '<div class="answers">'
                                        }
                                    }

                                }
                            }
                            html += '</p></div>'
                        }
                        html += '</div>' // div.answers
                        html += '</div>'
                        html += '<hr/>'

                    } // end if else
                } // end for
                commerce_log_text.append(html)

                if (gameDirection === 'backward') {
                    phase_obj = turn_obj['build_phase'];
                    for (let i = 0; i < phase_obj.length; i++) {
                        if (phase_obj[i]['building'] !== null) {
                            switch (phase_obj[i]['building']) {
                                case 'town':
                                    if (phase_obj[i]['finished']) {
                                        let node = jQuery('#node_' + phase_obj[i]['node_id']);
                                        paint_it_player_color(null, node);
                                        node.html('');

                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text + 1,
                                            'mineral': mineral_quantity_text + 0,
                                            'clay': clay_quantity_text + 1,
                                            'wood': wood_quantity_text + 1,
                                            'wool': wool_quantity_text + 1,
                                        });
                                        //                                        let str = 'node: ' + phase_obj[i]['node_id'] + ' | ' + 'type: ' + 'T' + '\r\n';
                                        //                                            textarea.text(textarea.text() + str);
                                    }
                                    break;
                                case 'city':
                                    if (phase_obj[i]['finished']) {
                                        let node = jQuery('#node_' + phase_obj[i]['node_id']);
                                        node.html('<i class="fa-solid fa-house"></i>');

                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text + 2,
                                            'mineral': mineral_quantity_text + 3,
                                            'clay': clay_quantity_text + 0,
                                            'wood': wood_quantity_text + 0,
                                            'wool': wool_quantity_text + 0,
                                        });

                                        //                                        let str = 'node: ' + phase_obj[i]['node_id'] + ' | ' + 'type: ' + 'C' + '\r\n';
                                        //                                            textarea.text(textarea.text() + str);
                                    }
                                    break;
                                case 'road':
                                    if (phase_obj[i]['finished']) {
                                        let road = '';
                                        if (phase_obj[i]['node_id'] < phase_obj[i]['road_to']) {
                                            road = jQuery('#road_' + phase_obj[i]['node_id'] + '_' + phase_obj[i]['road_to']);
                                        } else {
                                            road = jQuery('#road_' + phase_obj[i]['road_to'] + '_' + phase_obj[i]['node_id']);
                                        }
                                        paint_it_player_color(null, road);

                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text + 0,
                                            'mineral': mineral_quantity_text + 0,
                                            'clay': clay_quantity_text + 1,
                                            'wood': wood_quantity_text + 1,
                                            'wool': wool_quantity_text + 0,
                                        });
                                        //                                        let str = 'node: ' + phase_obj[i]['node_id'] + ' | ' + 'road_to: ' + phase_obj[i]['road_to'] + ' | ' + 'type: ' + 'R' + '\r\n'
                                        //                                            textarea.text(textarea.text() + str)
                                    }
                                    break;
                                case 'card':
                                    if (phase_obj[i]['finished']) {
                                        let card_div = jQuery(jQuery('#hand_P' + (actual_player_json) + ' .bottom_hand_row').children()[phase_obj[i]['card_effect']])
                                        let card_div_quantity = card_div.find('.' + card_div.data('id') + '_quantity')
                                        let card_div_increment = card_div.find('.increment')

                                        card_div_increment.removeClass(['fa-caret-up', 'fa-caret-down', 'fa-minus']);
                                        card_div.removeClass(['increased', 'decreased', 'neutral']);

                                        card_div_quantity.text(parseInt(card_div_quantity.text()) - 1)

                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text + 1,
                                            'mineral': mineral_quantity_text + 1,
                                            'clay': clay_quantity_text + 0,
                                            'wood': wood_quantity_text + 0,
                                            'wool': wool_quantity_text + 1,
                                        });
                                    }
                                    break;
                                case 'played_card':
                                    for (let i = 0; i < phase_obj.length; i++) {
                                        if (phase_obj[i]['development_card_played']) {
                                            off_development_card_played(phase_obj[i]['development_card_played'])
                                        }
                                    }
                                    break;
                                default:
                                    break;
                            }
                        }
                    }
                }
                break;
            case 2:
                phase_obj = turn_obj['build_phase'];

                for (let i = 0; i < phase_obj.length; i++) {
                    if (phase_obj[i]['building'] !== null) {
                        html += '<div>';
                        switch (phase_obj[i]['building']) {
                            case 'town':
                                if (phase_obj[i]['finished']) {
                                    let node = jQuery('#node_' + phase_obj[i]['node_id']);
                                    paint_it_player_color(actual_player_json, node);
                                    node.html('<i class="fa-solid fa-house"></i>');

                                    if (gameDirection === 'forward') {
                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text - 1,
                                            'mineral': mineral_quantity_text - 0,
                                            'clay': clay_quantity_text - 1,
                                            'wood': wood_quantity_text - 1,
                                            'wool': wool_quantity_text - 1,
                                        });
                                    }

                                    html += 'Building: Town | ' + 'Node: ' + phase_obj[i]['node_id'];
                                }
                                break;
                            case 'city':
                                if (phase_obj[i]['finished']) {
                                    let node = jQuery('#node_' + phase_obj[i]['node_id']);
                                    node.html('<i class="fa-solid fa-chess-rook"></i>');

                                    if (gameDirection === 'forward') {
                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text - 2,
                                            'mineral': mineral_quantity_text - 3,
                                            'clay': clay_quantity_text - 0,
                                            'wood': wood_quantity_text - 0,
                                            'wool': wool_quantity_text - 0,
                                        });
                                    }

                                    html += 'Building: City | ' + 'Node: ' + phase_obj[i]['node_id'];
                                }
                                break;
                            case 'road':
                                if (phase_obj[i]['finished']) {
                                    let road = '';
                                    if (phase_obj[i]['node_id'] < phase_obj[i]['road_to']) {
                                        road = jQuery('#road_' + phase_obj[i]['node_id'] + '_' + phase_obj[i]['road_to']);
                                    } else {
                                        road = jQuery('#road_' + phase_obj[i]['road_to'] + '_' + phase_obj[i]['node_id']);
                                    }
                                    paint_it_player_color(actual_player_json, road);

                                    if (gameDirection === 'forward') {
                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text - 0,
                                            'mineral': mineral_quantity_text - 0,
                                            'clay': clay_quantity_text - 1,
                                            'wood': wood_quantity_text - 1,
                                            'wool': wool_quantity_text - 0,
                                        });
                                    }
                                    html += 'Building: Road | ' + 'Node: ' + phase_obj[i]['node_id'] + ' | ' + 'Road_to: ' + phase_obj[i]['road_to'];
                                }
                                break;
                            case 'card':
                                let card_effects = ['Knight', 'Victory Point', 'Road Building', 'Year of plenty', 'Monopoly'];
                                if (phase_obj[i]['finished']) {
                                    let card_div = jQuery(jQuery('#hand_P' + actual_player_json + ' .bottom_hand_row').children()[phase_obj[i]['card_effect']])
                                    let card_div_quantity = card_div.find('.' + card_div.data('id') + '_quantity')
                                    let card_div_increment = card_div.find('.increment')

                                    // Se añade la clase caret-up y el color rojo para marcar el aumento de cartas
                                    card_div_increment.addClass('fa-caret-up');
                                    card_div.addClass('increased');

                                    if (gameDirection === 'forward') {
                                        changeHandObject(actual_player_json, {
                                            'cereal': cereal_quantity_text - 1,
                                            'mineral': mineral_quantity_text - 1,
                                            'clay': clay_quantity_text - 0,
                                            'wood': wood_quantity_text - 0,
                                            'wool': wool_quantity_text - 1,
                                        });
                                        card_div_quantity.text(parseInt(card_div_quantity.text()) + 1)
                                    }
                                    html += 'Building: Card | ' + 'Card Type: ' + card_effects[phase_obj[i]['card_effect']];
                                }
                                break;
                            case 'played_card':
                                if (phase_obj[i]['development_card_played'] && gameDirection === 'forward') {
                                    on_development_card_played(phase_obj[i]['development_card_played'])
                                }
                                break;
                            default:
                                break;
                        }
                        html += '</div>';
                    }
                }
                other_useful_info_text.append(html);
                if (gameDirection === 'backward') {
                    phase_obj = turn_obj['end_turn'];

                    if (phase_obj['development_card_played'] && phase_obj['development_card_played'].length) {
                        // console.log('SE JUEGA CARTA DE DESAROLLO AL INICIO DEL TURNO' + '| Ronda: ' + contador_rondas.val() + ' Turno: ' + contador_turnos.val())
                        // console.log(phase_obj)
                        off_development_card_played(phase_obj['development_card_played'][0])
                    }
                }
                break;
            case 3:
                phase_obj = turn_obj['end_turn'];
                let winner = '';

                if (phase_obj['development_card_played'] && phase_obj['development_card_played'].length && gameDirection === 'forward') {
                    // console.log('SE JUEGA CARTA DE DESAROLLO AL FINAL DEL TURNO' + '| Ronda: ' + contador_rondas.val() + ' Turno: ' + contador_turnos.val())
                    // console.log(phase_obj)
                    on_development_card_played(phase_obj['development_card_played'][0])
                }

                for (let i = 0; i < 4; i++) {
                    jQuery('#puntos_victoria_J' + (i + 1)).text(phase_obj['victory_points']['J' + i])
                    if (parseInt(phase_obj['victory_points']['J' + i]) >= 10) {
                        winner = 'J' + (i + 1) + ' GANA'
                    }
                }

                if (winner !== '' && contador_turnos.val() >= 4) {
                    alert(winner);
                }

                if (gameDirection === 'backward') {
                    let round = game_obj['game']['round_' + (contador_rondas.val() - 1)];
                    let next_player = actual_player_json + 1; // 1 - 4

                    if (next_player > 3) {
                        next_player = 0;
                        round = game_obj['game']['round_' + contador_rondas.val()]; // Se pasa de ronda y se le devuelve el turno al jugador 0
                    }

                    let next_turn_obj = round['turn_P' + next_player];
                    let next_phase_obj = next_turn_obj['start_turn'];
                    let diceroll = turn_obj['start_turn']['dice'];
                    diceroll_div.text('Diceroll: ' + diceroll);

                    if (next_phase_obj['development_card_played'] && next_phase_obj['development_card_played'].length) {
                        off_development_card_played(next_phase_obj['development_card_played'][0])
                    }
                }
                break;

            default:
                break;
        } // switch
    });


    //-------------------------------------------------
    // TODO: hacer solo hasta turno 0, fase 0
    ronda_previa_btn.off().on('click', function (e) {
        for (let i = 0; i < 4; i++) {
            turno_previo_btn.click();
        }
    });
    ronda_siguiente_btn.off().on('click', function (e) {
        for (let i = 0; i < 4; i++) {
            turno_siguiente_btn.click();
        }
    });

    //-------------------------------------------------
    // TODO: hacer solo hasta fase 0
    turno_previo_btn.off().on('click', function (e) {
        for (let i = 0; i < 4; i++) {
            fase_previa_btn.click();
        }
    });
    turno_siguiente_btn.off().on('click', function (e) {
        for (let i = 0; i < 4; i++) {
            fase_siguiente_btn.click();
        }
    });

    //-------------------------------------------------
    fase_previa_btn.off().on('click', function (e) {
        gameDirection = 'backward';
        let value = parseInt(contador_fases.val());
        contador_fases.val(value - 1).change();
    });
    fase_siguiente_btn.off().on('click', function (e) {
        gameDirection = 'forward';
        let value = parseInt(contador_fases.val());
        contador_fases.val(value + 1).change();
    });

    millis_for_play.off().on('change', function (e) {
        jQuery('#millis_seleccionados').val(millis_for_play.val());
    });

    play_btn.off().on('click', function (e) {
        let _this = $(this);
        let _i = _this.find('i');

        if (_i.hasClass('fa-play')) {
            _i.removeClass('fa-play').addClass('fa-pause');

            _this.attr('title', 'Pause')

            //                    playIntervalNumber = setInterval(function() {
            //                        turno_siguiente_btn.click()
            //                    }, 500)
            playIntervalNumber = setInterval(function () {
                fase_siguiente_btn.click()
            }, millis_for_play.val())

        } else {
            _this.attr('title', 'Play')

            _i.removeClass('fa-pause').addClass('fa-play');
            clearInterval(playIntervalNumber)
        }

        $(function () {
            _this.tooltip('dispose')
            _this.tooltip()
        })
    })
}

function changeHandObject(player, hand_obj) {
    //TODO: Debería de alguna manera mostrar que materiales se han actualizado. Si son iguales no deberían de recalcarse
    $('#hand_P' + player + ' .cereal_quantity').text(hand_obj['cereal']).change();
    $('#hand_P' + player + ' .clay_quantity').text(hand_obj['clay']).change();
    $('#hand_P' + player + ' .wood_quantity').text(hand_obj['wood']).change();
    $('#hand_P' + player + ' .wool_quantity').text(hand_obj['wool']).change();
    $('#hand_P' + player + ' .mineral_quantity').text(hand_obj['mineral']).change();
}

// utilities
function paint_it_player_color(player, object_to_paint) {
    object_to_paint = jQuery(object_to_paint);
    object_to_paint.css('color', 'black')
    switch (player) {
        case 0:
            object_to_paint.css('background', 'lightcoral') //.css('border', '1px solid black');
            break;
        case 1:
            object_to_paint.css('background', 'lightblue') //.css('border', '1px solid black');
            break;
        case 2:
            object_to_paint.css('background', 'lightgreen') //.css('border', '1px solid black');
            break;
        case 3:
            object_to_paint.css('background', 'lightyellow') //.css('border', '1px solid black');
            break;
        default:
            object_to_paint.css('background', 'none')
            break;
    }
}

function on_development_card_played(card) {
    // TODO: mostrar dentro de "otra información útil" que se ha jugado una carta de desarrollo
    jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card']).removeClass(['increased', 'neutral', 'decreased']).addClass('decreased')
    jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card'] + ' .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-down')
    let quantity = jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card'] + '_quantity')
    quantity.text(parseInt(quantity.text()) - 1).change()

    switch (card['played_card']) {
        case 'knight':
            //console.log(quantity.text(parseInt(quantity.text()) - 1));
            break;
        case 'victory_point':
            break;
        case 'failed_victory_point':
            break;

        case 'monopoly':
            material_chosen = ''
            switch (card['material_chosen']) {
                case 0:
                    material_chosen = 'cereal';
                    break;
                case 1:
                    material_chosen = 'mineral';
                    break;
                case 2:
                    material_chosen = 'clay';
                    break;
                case 3:
                    material_chosen = 'wood';
                    break;
                case 4:
                    material_chosen = 'wool';
                    break;
                default:
                    break;
            }

            for (let i = 0; i < 4; i++) {
                changeHandObject(i, card['hand_P' + i]);

                if (material_chosen != '') {
                    jQuery('#hand_P' + i + ' .' + material_chosen).addClass('decreased');
                    jQuery('#hand_P' + i + ' .' + material_chosen + ' .increment').addClass('fa-caret-down');
                }
            }

            if (material_chosen != '') {
                jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + material_chosen).removeClass('decreased').addClass('increased');
                jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + material_chosen + ' .increment').removeClass('fa-caret-down').addClass('fa-caret-up');
            }
            break;

        case 'year_of_plenty':
            break;
        case 'road_building':
            break;

        case 'none':
        default:
            break;
    }
}

function off_development_card_played(card) {
    // TODO: deshacer carta de desarrollo jugada
    jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card']).removeClass(['increased', 'neutral', 'decreased']).addClass('increased')
    jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card'] + ' .increment').removeClass(['fa-caret-up', 'fa-minus', 'fa-caret-down']).addClass('fa-caret-up')
    let quantity = jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + card['played_card'] + '_quantity')
    quantity.text(parseInt(quantity.text()) + 1).change()

    switch (card['played_card']) {
        case 'knight':
            // console.log(quantity.text(parseInt(quantity.text()) + 1));
            break;
        case 'victory_point':
            break;
        case 'failed_victory_point':
            break;

        case 'monopoly':
            let material_chosen_array = ['cereal', 'mineral', 'clay', 'wood', 'wool'];
            material_chosen = material_chosen_array[card['material_chosen']];

            for (let i = 0; i < 4; i++) {
                changeHandObject(i, card['hand_P' + i]);

                if (material_chosen != '') {
                    jQuery('#hand_P' + i + ' .' + material_chosen).addClass('increased');
                    jQuery('#hand_P' + i + ' .' + material_chosen + ' .increment').addClass('fa-caret-up');
                }
            }

            if (material_chosen != '') {
                jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + material_chosen).removeClass('increased').addClass('decreased');
                jQuery('#hand_P' + (jQuery('#contador_turnos').val() - 1) + ' .' + material_chosen + ' .increment').removeClass('fa-caret-up').addClass('fa-caret-down');
            }
            break;

        case 'year_of_plenty':
            break;
        case 'road_building':
            break;

        case 'none':
        default:
            break;
    }
}

function deleteCaretStyling() {
    jQuery('.increment').removeClass(['fa-caret-up', 'fa-caret-down', 'fa-minus']);
    jQuery('.increment').parent().removeClass(['increased', 'decreased', 'neutral']);
}

function setup() {
    //            nodeSetup();
    terrainSetup();
    addSetupBuildings();
}

// init()
window.addEventListener('load', function () {
    init_events();
}, false);
