'use strict';

/* App Module */

var analys = angular.module( 'analys', [
  'ngResource',
  'restangular',
  'analys.submissionsCreate',
  'analys.submissionsView',
  'analys.workflowCreate',
  'analys.workflowView',
  'analys.users',
  'analys.preferences',
  'analys.plugins',
  'analys.dashboard',
  'analys.results',
  'analys.search',
  'analys.auth'
])

.config( function myAppConfig ( $routeProvider ) {
  $routeProvider.otherwise({ redirectTo: '/login' });
})

analys.service('messageService', function(){
    var messages = []
    this.addMessage = function(message){
        switch(message['type']){
            case "error":
                message['type'] = 'alert-danger';
                break;
            case "warning":
                message['type'] = 'alert-warning';
                break;
            case "info":
                message['type'] = 'alert-info';
                break;
            case "success":
                message['type'] = 'alert-success';
                break;
            default:
                message = {"type": "alert-danger", "value": "There was an internal error"};
                break;
        }
        messages.push(message);

    }
    this.dismissMessage = function(index){
        messages.splice(index, 1);    
    }

    this.getMessages = function(){
        return messages;
    }
});

function MsgCtrl($scope, messageService){
    $scope.messages = messageService.getMessages();
}
