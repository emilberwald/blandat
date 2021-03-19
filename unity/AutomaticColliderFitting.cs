using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using UnityEditor;
using UnityEngine;
using Unity.EditorCoroutines.Editor;


public class AutomaticColliderFitting : ScriptableWizard
{
    [field: SerializeField]
    public SkinnedMeshRenderer SkinnedMeshRenderer { get; set; }

    [field: SerializeField]
    public Cloth Cloth { get; set; }

    [MenuItem("Tools/Fit Colliders To Bones")]
    static void CreateWizard()
    {
        CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
        CultureInfo.CurrentUICulture = CultureInfo.InvariantCulture;
        DisplayWizard<AutomaticColliderFitting>("Automatic Collider Fitting", "Fit");
    }

    IEnumerator ProcessBones()
    {
        var queriesHitBackfaces = Physics.queriesHitBackfaces;

        List<CapsuleCollider> colliders = new List<CapsuleCollider>();

        var meshCollider = this.SkinnedMeshRenderer.transform.root.gameObject.AddComponent<MeshCollider>();
        try
        {
            Physics.queriesHitBackfaces = true;

            meshCollider.sharedMesh = this.SkinnedMeshRenderer.sharedMesh;

            var maxDistance = this.SkinnedMeshRenderer.bounds.size.magnitude;

            foreach(var bone in this.SkinnedMeshRenderer.bones)
            {
                if(bone == null) continue;

                List<Vector3> X = new List<Vector3> { Vector3.left, Vector3.right };
                List<Vector3> Y = new List<Vector3> { Vector3.up, Vector3.down };
                List<Vector3> Z = new List<Vector3> { Vector3.forward, Vector3.back };

                var resultX = RayCast(meshCollider, maxDistance, bone, X).ToList();
                var resultY = RayCast(meshCollider, maxDistance, bone, Y).ToList();
                var resultZ = RayCast(meshCollider, maxDistance, bone, Z).ToList();

                var closestToBoneX = resultX.Where(x => x.hit.collider != null).Select(x => (x.hit.distance, x)).DefaultIfEmpty().Min().x;
                var closestToBoneY = resultY.Where(x => x.hit.collider != null).Select(x => (x.hit.distance, x)).DefaultIfEmpty().Min().x;
                var closestToBoneZ = resultZ.Where(x => x.hit.collider != null).Select(x => (x.hit.distance, x)).DefaultIfEmpty().Min().x;

                var tentative = new List<(Vector3 direction, Ray ray, RaycastHit hit)> { closestToBoneX, closestToBoneY, closestToBoneZ }.Where(x => x.direction != default).ToList();
                if(tentative.Count < 2) { continue; }

                var closest = tentative.Select(x => (x.hit.distance, x)).Min().x;
                tentative.Remove(closest);
                var furthest = tentative.Select(x => (x.hit.distance, x)).Max().x;


                var collider = Undo.AddComponent<CapsuleCollider>(bone.gameObject);
                collider.center = Vector3.zero;
                collider.radius = collider.transform.InverseTransformPoint(closest.hit.point).magnitude;
                collider.height = collider.transform.InverseTransformPoint(furthest.hit.point).magnitude;
                if(furthest.direction == Vector3.left || furthest.direction == Vector3.right) { collider.direction = 0; }
                if(furthest.direction == Vector3.up || furthest.direction == Vector3.down) { collider.direction = 1; }
                if(furthest.direction == Vector3.forward || furthest.direction == Vector3.back) { collider.direction = 2; }

                bool overlapped = Physics.ComputePenetration(
                    collider, collider.transform.position, collider.transform.rotation,
                    meshCollider, meshCollider.transform.position, meshCollider.transform.rotation,
                    out Vector3 direction, out float distance
                );

                if(overlapped)
                {
                    Selection.objects = default;
                    Selection.activeObject = collider;
                    SceneView.lastActiveSceneView.LookAtDirect(collider.transform.position, SceneView.lastActiveSceneView.rotation);
                    SceneView.RepaintAll();
                    yield return null;

                    if(EditorUtility.DisplayDialog("CapsuleCollider overlaps MeshCollider.", "Action for CapsuleCollider?", "Add", "Remove"))
                    {
                        colliders.Add(collider);
                    }
                    else
                    {
                        DestroyImmediate(collider);
                    }
                }
                else
                {
                    colliders.Add(collider);
                }
            }
        }
        finally
        {
            DestroyImmediate(meshCollider);
            // Restore setting
            Physics.queriesHitBackfaces = queriesHitBackfaces;
        }

        if(this.Cloth != null)
        {
            this.Cloth.capsuleColliders = colliders.ToArray();
        }

        static IEnumerable<(Vector3 direction, Ray ray, RaycastHit hit)> RayCast(MeshCollider meshCollider, float maxDistance, Transform bone, List<Vector3> X)
        {
            foreach(var direction in X)
            {
                var ray = new Ray(bone.position, bone.TransformDirection(direction));
                meshCollider.Raycast(ray, out RaycastHit raycastHit, maxDistance);
                yield return (direction, ray, raycastHit);
            }
        }
    }

    /// <summary>
    /// Fit
    /// </summary>
    void OnWizardCreate()
    {
        Undo.RegisterCompleteObjectUndo(this.SkinnedMeshRenderer, "Automatic Collider Fitting");
        Debug.Log("Automatic Collider Fitting.", this.SkinnedMeshRenderer);

        co = EditorCoroutineUtility.StartCoroutineOwnerless(this.ProcessBones());
    }

    private EditorCoroutine co;

    void OnWizardUpdate()
    {
        this.helpString = "Fits colliders to mesh.";
    }
}
