function get_current_date_time() {
    var date = new Date();
    var raw_string = date.toLocaleString();
    // Replace slashes to dashes, remove all Chinese characters.
    var date_string = raw_string.replace(/\//g, '-').replace(/[\u4e00-\u9fa5]/g, '');

    return date_string;
}
