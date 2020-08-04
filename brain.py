

import image_detection_yolo
import speech_to_text


def brain(data):

    if data and ("what is this" in data or "what is" in data or "do you see" in data):
        speech_to_text.SpeakText("Let me see")
        statement = image_process("./current_image.jpg")
        speech_to_text.SpeakText(statement)
    elif data and ("describe" in data or "descibe surrounding" in data):
        #Here let's integrate the desctibe call
        pass
    else:
        speech_to_text.SpeakText("Sorry! I don't understand")

def image_process(image):
    
    classes = '/tmp/coco_classes.txt'
    anchors = '/tmp/yolo_anchors.txt' 
    model = '/tmp/yolo.h5'
    print("processing 1")
    with open(classes) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]

    with open(anchors) as f:
        anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        anchors = np.array(anchors).reshape(-1, 2)
    print("processing 2")

    converter = tf.lite.TFLiteConverter.from_keras_model_file(model)
    yolo_model = converter.convert()
    #yolo_model = load_model(model)
    print("processing 3")

    score_threshold = .3
    iou_threshold = .5

    sess = K.get_session()
    print("processing 4")

    # Check if model is fully convolutional, assuming channel last order.
    model_image_size = yolo_model.layers[0].input_shape[1:3]
    is_fixed_size = model_image_size != (None, None)
    print("processing 5")

    # Generate output tensor targets for filtered bounding boxes.
    # TODO: Wrap these backend operations with Keras layers.
    yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))
    print("processing 6")
    input_image_shape = K.placeholder(shape=(2, ))
    print("processing 7")
    boxes, scores, classes = yolo_eval(
        yolo_outputs,
        input_image_shape,
        score_threshold=score_threshold,
        iou_threshold=iou_threshold)
    print("processing 8")

    objs = evaluate_img(img_name)
    return(form_speech_string(objs))


def yolo_head(feats, anchors, num_classes):
    """Convert final layer features to bounding box parameters.
    """
    num_anchors = len(anchors)
    # Reshape to batch, height, width, num_anchors, box_params.
    anchors_tensor = K.reshape(K.variable(anchors), [1, 1, 1, num_anchors, 2])

    # Dynamic implementation of conv dims for fully convolutional model.
    conv_dims = K.shape(feats)[1:3]  # assuming channels last
    # In YOLO the height index is the inner most iteration.
    conv_height_index = K.arange(0, stop=conv_dims[0])
    conv_width_index = K.arange(0, stop=conv_dims[1])
    conv_height_index = K.tile(conv_height_index, [conv_dims[1]])

    # conv_width_index = K.repeat_elements(conv_width_index, conv_dims[1], axis=0)
    conv_width_index = K.tile(
        K.expand_dims(conv_width_index, 0), [conv_dims[0], 1])
    conv_width_index = K.flatten(K.transpose(conv_width_index))
    conv_index = K.transpose(K.stack([conv_height_index, conv_width_index]))
    conv_index = K.reshape(conv_index, [1, conv_dims[0], conv_dims[1], 1, 2])
    conv_index = K.cast(conv_index, K.dtype(feats))

    feats = K.reshape(
        feats, [-1, conv_dims[0], conv_dims[1], num_anchors, num_classes + 5])
    conv_dims = K.cast(K.reshape(conv_dims, [1, 1, 1, 1, 2]), K.dtype(feats))

    box_xy = K.sigmoid(feats[..., :2])
    box_wh = K.exp(feats[..., 2:4])
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.softmax(feats[..., 5:])

    # Adjust preditions to each spatial grid point and anchor size.
    # Note: YOLO iterates over height index before width index.
    box_xy = (box_xy + conv_index) / conv_dims
    box_wh = box_wh * anchors_tensor / conv_dims

    return box_xy, box_wh, box_confidence, box_class_probs
