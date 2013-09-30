angular.module( 'analys.auth', [
 
])

.config(function config( $routeProvider ) {
  $routeProvider.when( '/login', {
    controller: 'AuthCtrl',
    templateUrl: 'static/app/auth/login.tpl.html'
  });
})

.controller( 'AuthCtrl', function AuthCtrl( $scope ) {
  
})

;
