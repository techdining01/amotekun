class MapPermissionManager{

    constructor(role){

        this.role=role;

    }

    initialize(){

        layerRegistry.all().forEach(layer=>{

            if(

                layer.roles.includes(this.role)

            ){

                layer.loader();

            }

        });

    }

}

window.permissionManager=null;