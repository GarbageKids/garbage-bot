(function(angular, jquery) {

	// APP 
    let app = angular.module('green_bot', []);

    // KEYBOARD EVENT
    app.directive('onEnter', function() {

        var linkFn = function(scope, element, attrs) {
            element.bind("keypress", function(event) {
                if (event.which === 13) {
                    scope.$apply(function() {
                        scope.$eval(attrs.onEnter);
                    });
                    event.preventDefault();
                }
            });
        };
        return {
            link: linkFn
        };
    });

    // CHAT CONTROLLER
    app.controller('ChatCtrl', function($scope, $timeout) {

        let socket = io('/');
        $scope.chat = [];

        socket.on('reply', function(data) {
            data = JSON.parse(data);
            $scope.chat.push(data);
            $scope.$digest();

            let scroll = jquery('.chat-body');
            scroll.animate({ scrollTop: scroll.prop('scrollHeight') }, 0);

        });
        $scope.sent = function() {
            if (jquery.trim($scope.msg) !== '') {
                let data = { 'msg': $scope.msg, 'name': 'Хэрэглэгч' };
                socket.emit('message', data);
                $scope.chat.push(data);
                $scope.msg = '';
                let scroll = jquery('.chat-body');
                scroll.animate({ scrollTop: scroll.prop('scrollHeight') }, 0);
            } else {
                $scope.error = true;
                $timeout(function() {
                    jquery(".alert").removeClass("animated fadeInRight");
                    jquery(".alert").addClass("animated fadeOutRight");
                    $timeout(function() {
                        jquery(".alert").addClass("animated fadeInRight");
                        $scope.error = false;
                    }, 1000);
                }, 2000);
            }
        }
    });
})(angular, $);
