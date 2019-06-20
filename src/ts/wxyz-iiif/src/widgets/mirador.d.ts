declare module 'mirador' {
  const MiradorStatic: IMirador;

  export default MiradorStatic;

  export interface IMirador {
    viewer(opts: Mirador.IOptions): Mirador.IViewer;
  }

  export namespace Mirador {
    export interface IViewer {
      store: IStore;
      actions: any;
    }

    export interface IStore {
      getState(...options: any): any;
      dispatch(...options: any): any;
      subscribe(...options: any): any;
    }

    export interface IOptions {
      /**
        id: ID of HTML element that will be used by Mirador
      */
      id: string;
      /**
        buildPath: Assign the default location of the Mirador directory
      */
      /**
        data: Array of manifest URIs to load into Mirador. Each item in the array must use the following format: { "manifestUri": "[Manifest URI]", "location": "[Institution Name]"}
      */
      /**
        saveSession: [true, false] Whether or not to save a user's session to local storage
      */
      /**
        layout: Default configuration of slots on load (Default: '1x1')
      */
      /**
        annotationEndpoint: Required to allow annotation creation. To store annotations locally, use { "name":"Local Storage", "module": "LocalStorageEndpoint" }
      */
      /**
        openManifestsPage: [true, false] Whether or not Mirador should display the manifests page on load. It is only valid if no windowObjects have been initialized. If there are multiple slots, it will be bound to the first slot and the selected manifest will open in that slot
      */
      /**
        manifestsPanel.name: ['Classic Mirador Manifests Panel'] A description of the manifest selection panel enabled for Mirador. This is only a reminder --- the actual panel type is specified in manifestsPanel.module.
      */
      /**
        manifestsPanel.module: ['ManifestsPanel', 'CollectionTreeManifestsPanel'] The class name of the manifest selection panel enabled for Mirador. ManifestsPanel is the classic manifests-only panel, and CollectionTreeManifestsPanel is an expanded version of ManifestsPanel with an additional collection navigation tree. Aside from the above, it is also possible to implement other panel types in the source code (see js/src/viewer/manifestsPanel.js and js/src/viewer/collectionTreeManifestsPanel.js as examples) and specify its class name here.
      */
      /**
        manifestsPanel.options: Additional options passed into the selected manifest panel object. May be useful when building a custom manifest selection panel type.
      */
      /**
        mainMenuSettings.show: [true, false] Whether or not to display the top menu
      */
      /**
        mainMenuSettings.buttons: Control individual buttons in the top menu
      */
      /**
        mainMenuSettings.buttons.bookmark: [true, false] Controls display of 'Bookmark' in the top menu
      */
      /**
        mainMenuSettings.buttons.layout: [true, false] Controls display of 'Change Layout' in the top menu
      */
      /**
        mainMenuSettings.buttons.options: [true, false] Controls display of 'Options' in the top menu. Currently, 'Options' has not been implemented.
      */
      /**
        mainMenuSettings.buttons.fullScreenViewer: [true, false] Controls display of the 'Full Screen' button in the top menu, which allows for fullscreen view of Mirador
      */
      /**
        showAddFromURLBox: [true, false] Controls display of "Add new object from URL" on manifest listing page
      */
      /**
        autoHideControls: [true, false] Controls whether to hide buttons when the cursor is away from the canvas
      */
      /**
        fadeDuration: [400] Number of milliseconds to take to fade out buttons when the cursor is away from the canvas (requires enabling autoHideControls)
      */
      /**
        timeoutDuration [3000] Number of milliseconds that the cursor must spend away from the canvas before the buttons begin fading out (requires enabling autoHideControls)
      */
    }
  }
}
