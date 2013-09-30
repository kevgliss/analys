/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'analys.submissionsView', [
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $routeProvider ) {
  $routeProvider.when( '/submissions/view', {
    controller: 'SubmissionsViewCtrl',
    templateUrl: '/static/app/submissions/view/view.tpl.html'
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'SubmissionsViewCtrl', function SubmissionsViewController( $scope, $http ) {
    return $http.get('/1/submissions').success(function(res){
        for (var sub in res){
            var completed_tasks = 0;
            
            for (var task in res[sub]['tasks']){
                if (res[sub]['tasks'][task]['status'] === 'Completed'){
                    completed_tasks++;
                };
            };
            res[sub]['completed_tasks'] = completed_tasks;
            if(typeof res[sub]['tasks'] === 'undefined'){
                res[sub]['total_tasks'] = 0;
            } else {
                res[sub]['total_tasks'] = res[sub]['tasks'].length;
            }
        }; 
        $scope.subs = res;
    });

    $scope.oid_to_date = function(oid){
        debugger;
        return new Date(parseInt(oid.toString().slice(0,8), 16)*1000);
    };
})
