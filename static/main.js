var hiddenClass = 'hidden';
var shownClass = 'toggled-from-hidden';

function driverSectionHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === hiddenClass) {
            child.className = shownClass;
        }
    }
}

function driverSectionEndHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === shownClass) {
            child.className = hiddenClass;
        }
    }
}

(function() {
    var driverSections = document.getElementsByClassName('drivername');
    for(var i = 0; i < driverSections.length; i++) {
        driverSections[i].addEventListener('mouseover', driverSectionHover);
        driverSections[i].addEventListener('mouseout', driverSectionEndHover);
    }
}());
