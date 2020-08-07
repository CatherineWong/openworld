// Initial state
var CURRENT_SCALING_CONSTANT = 25;
var CURRENT_WORLD = undefined;
var CURRENT_AISLE = undefined;

var PREVIEW_SCALING_CONSTANT = 6;
var NUM_TO_PREVIEW = 6;

function fillAisleViewWithData(jq_aisle, world, aisle, scaling_constant) {
  // Add shelves.
  var shelf_width = Math.floor(scaling_constant * world.aisle_size);
  var shelf_height = Math.floor((scaling_constant * world.aisle_size) / world.num_shelves_per_aisle);
  jq_aisle_wrapper = $('<div class="aisle_wrapper"></div>');
  for (var shelf_id = 0; shelf_id < aisle.num_shelves; shelf_id++) {
    shelf_name = "shelf_" + aisle.id + "_" + shelf_id + "_" + scaling_constant
    jq_shelf = $('<div id="' + shelf_name +  '" class="shelf"></div>');
    jq_shelf.css('height', shelf_height + 'px');
    jq_shelf.css('width', shelf_width + 'px');
    jq_shelf.appendTo(jq_aisle_wrapper);
  }
  jq_aisle_wrapper.appendTo(jq_aisle);

  // Add boxes.
  for (var box_id in aisle.boxes) {
    box = aisle.boxes[box_id];
    var box_width = Math.floor(scaling_constant * box.width);
    var box_height = Math.floor(scaling_constant * box.height);
    var box_spacing = Math.floor(scaling_constant * box.pos[1]);
    
    jq_box = $('<div id="box_' + box.id + '" class="box"></div>');
    jq_box.css('height', box_height + 'px');
    jq_box.css('width', box_width + 'px');
    jq_box.css('left', box_spacing + 'px');
    
    if (box.id === CURRENT_TASK.target) {
      jq_box.css('background-color', 'sandybrown');
    }
    
    shelf_name = "shelf_" + aisle.id + "_" + box.pos[0] + "_" + scaling_constant
    jq_shelf = jq_aisle.find('#' + shelf_name);
    jq_box.appendTo(jq_shelf);
  }
}

function fillInstructionView() {
  jq_instruction = $('#current_instruction');
  jq_instruction.html(CURRENT_TASK.instruction);
}

function fillCurrentAisleView() {
    $('#current_aisle_view').html(''); // Reset
    jq_aisle = $('#current_aisle_view');
    fillAisleViewWithData(jq_aisle, CURRENT_WORLD, CURRENT_AISLE, CURRENT_SCALING_CONSTANT);
    $('#current_aisle_id_display').html(CURRENT_AISLE.id + 1);
    $('#total_aisle_count_display').html(CURRENT_WORLD.num_aisles);
}

function fillPreviewView() {
  // Fill the current aisle preview.
    $('#current_aisle_preview').html(''); 
    jq_aisle = $('#current_aisle_preview');
    fillAisleViewWithData(jq_aisle, CURRENT_WORLD, CURRENT_AISLE, PREVIEW_SCALING_CONSTANT);
  // Fill the previous aisles if they exist.
  $('#previous_aisles_preview').html(''); 
  jq_aisle = $('#previous_aisles_preview');
  for (var i = NUM_TO_PREVIEW; i > 0; i--) {
    previous_aisle_id = CURRENT_AISLE.id - i;
    if (previous_aisle_id >= 0) {
      fillAisleViewWithData(jq_aisle, CURRENT_WORLD, CURRENT_WORLD.aisles[previous_aisle_id], PREVIEW_SCALING_CONSTANT);
    } else {
      //Dummy aisles.
      var dummy_aisle_size = Math.floor(PREVIEW_SCALING_CONSTANT * CURRENT_WORLD.aisle_size);
      jq_dummy_aisle = $('<div class="aisle_wrapper"></div>');
      jq_dummy_aisle.css('height', dummy_aisle_size + 'px');
      jq_dummy_aisle.css('width', dummy_aisle_size + 'px');
      jq_dummy_aisle.css('border', '1px solid black');
      jq_dummy_aisle.appendTo(jq_aisle);
    }
  }
  
  // Fill the next aisles if they exist.
  $('#next_aisles_preview').html(''); 
  jq_aisle = $('#next_aisles_preview');
  for (var i = 0; i < NUM_TO_PREVIEW; i++) {
    next_aisle_id = CURRENT_AISLE.id + i + 1;
    if (next_aisle_id < CURRENT_WORLD.num_aisles) {
      fillAisleViewWithData(jq_aisle, CURRENT_WORLD, CURRENT_WORLD.aisles[next_aisle_id], PREVIEW_SCALING_CONSTANT);
    } else {
      //Dummy aisles.
      var dummy_aisle_size = Math.floor(PREVIEW_SCALING_CONSTANT * CURRENT_WORLD.aisle_size);
      jq_dummy_aisle = $('<div class="aisle_wrapper"></div>');
      jq_dummy_aisle.css('height', dummy_aisle_size + 'px');
      jq_dummy_aisle.css('width', dummy_aisle_size + 'px');
      jq_dummy_aisle.css('border', '1px solid black');
      jq_dummy_aisle.appendTo(jq_aisle);
    }
  }
}

function showNextAisle() {
  current_aisle_id = CURRENT_AISLE.id;
  if (current_aisle_id == (CURRENT_WORLD.aisles.length - 1)) {
    return;
  }
  CURRENT_AISLE = CURRENT_WORLD.aisles[current_aisle_id + 1];
  fillCurrentAisleView();
  fillPreviewView();
}

function showPreviousAisle() {
  current_aisle_id = CURRENT_AISLE.id;
  if (current_aisle_id == 0) {
    return;
  }
  CURRENT_AISLE = CURRENT_WORLD.aisles[current_aisle_id - 1];
  fillCurrentAisleView();
  fillPreviewView();
}

function loadJSONTask(task) {
    $('#modal_bg').hide();
    console.log(task);
    
    // Load the current aisle.
    CURRENT_TASK = task;
    CURRENT_WORLD = task.world;
    CURRENT_AISLE = task.world.aisles[task.location];
    fillCurrentAisleView();
    fillPreviewView();
    fillInstructionView();
}

function loadTaskFromFile(e) {
    var file = e.target.files[0];
    if (!file) {
        errorMsg('No file selected');
        return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
        var contents = e.target.result;

        try {
            contents = JSON.parse(contents);
            if ("world" in contents) {
              task = contents
            } else {
              task = {
                "world" : contents,
                "location" : 0,
                "instruction" : "No instruction given."
              }
            }
        } catch (e) {
            errorMsg('Error loading contenst');
            return;
        }
        loadJSONTask(task);
    };
    reader.readAsText(file);
}

$(document).ready(function () {
    $('.load_task').on('change', function(event) {
        loadTaskFromFile(event);
    });

    $('.load_task').on('click', function(event) {
      event.target.value = "";
    });
    
    document.onkeydown = function(e) {
    switch(e.which) {
        case 37: // left
        showPreviousAisle();
        break;
        case 39: // right
        showNextAisle();
        break;
        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
};
});