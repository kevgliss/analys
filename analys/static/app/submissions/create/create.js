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
angular.module( 'analys.submissionsCreate', [
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $routeProvider ) {
  $routeProvider.when( '/submissions/create', {
    controller: 'SubmissionsCreateCtrl',
    templateUrl: '/static/app/submissions/create/create.tpl.html'
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'SubmissionsCreateCtrl', function CreateController( $scope, messageService ) {

})

function AttachmentController( $scope, $http, messageService ){
    $scope.submissions = [];
    $scope.progressVisible = false;
    //TODO filter out attachements bigger than 16mb
    $scope.setFiles = function(element) {
        $scope.$apply(function(scope) {
          // Turn the FileList object into an Array
            for (var i = 0; i < element.files.length; i++) {
              element.files[i].resource = element.files[i].name;
              if (element.files[i].size > (1024 * 1024)) {
                element.files[i].size = (element.files[i].size / 1024 / 1024) + "MB";
              } else {
                element.files[i].size = (element.files[i].size / 1024) + "KB";
              }  
              $scope.submissions.push(element.files[i]);
              $scope.totalSize = $scope.totalSize + element.files[i].size;
            }
          });
        };


    //TODO get actual owner instead of hardcoding
    $scope.setUrls = function(element){
          var urls = [];
          urls = element.value.split(",");
            for (var i = 0; i < urls.length; i++) {
              $scope.submissions.push({"resource": urls[i], "type": "url", "owner": "kglisson"})
            }
          element.value = "";
        };

    $scope.removeSubmission = function(index){
          $scope.submissions.splice(index,1);
    };  

    $scope.uploadSubmission = function() {
        $scope.options = []
        for (var i = $scope.submissions.length - 1; i >= 0; --i) {
              var sub = $scope.submissions[i];
              if (sub["type"] === "url"){
                  sub = sub['resource'];
              }

              $http({
                         url: '/1/submissions',
                         method: 'POST',
                         headers: { 'Content-Type': false, 'Accept': 'application/json' },
                         //This method will allow us to change how the data is sent up to the server
                         // for which we'll need to encapsulate the model data in 'FormData'
                         transformRequest: function (data) {
                                var formData = new FormData();
                                //need to convert our json object to a string version of json otherwise
                                // the browser will do a 'toString()' on the object which will result 
                                // in the value '[Object object]' on the server.
                                formData.append("owner", "kglisson");
                                //now add all of the assigned files
                                //add each file to the form data and iteratively name them
                                formData.append("resource", sub);
                                return formData;
                            },
                            //Create an object that contains the model and files which will be transformed
                            // in the above transformRequest method
                            data: { files: sub } 
                    }).success(function (data, status, headers, config) {
                        $scope.removeSubmission(i);
                        $scope.option = {"owner": data["owner"], 
                                         "submission_id": data["_id"]["$oid"], 
                                         "resource": data["resource"],
                                         "resource_type": data["resource_type"],
                                         "plugins": {}}
                        
                        angular.forEach(data.plugins, function(pluginOptions, pluginName){
                            $scope.option["plugins"][pluginName] = {};
                            angular.forEach(pluginOptions, function (optionValues, optionName){
                                $scope.option["plugins"][pluginName][optionName] = {}
                                angular.forEach(optionValues, function(optionValue, fieldName){
                                    $scope.option["plugins"][pluginName][optionName][fieldName] = optionValue;
                                });
                            });
                        }); 
                        $scope.options.push($scope.option);
                    }).error(function (data, status, headers, config) {

                        messageService.addMessage(data);
                    });
        }
    }


    $scope.createTasks = function(){
        options = $scope.options;
        for (var i = $scope.options.length - 1; i >= 0; --i){
            $http({
                url: '/1/tasks',
                method: 'POST',
                data: options[i]
            }).success(function(data, status, headers, config){
                $scope.options.splice(i,1);
                messageService.addMessage(data);
                
            }).error(function (data, status, headers, config){
                messageService.addMessage(data);
            });


        }
    }

}
