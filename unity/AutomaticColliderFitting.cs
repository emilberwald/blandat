using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using UnityEditor;
using UnityEngine;
using Unity.EditorCoroutines.Editor;
using System;
using System.Reflection;

public static class AutomaticColliderFittingExtensions
{
    internal static int GetDirection(this CapsuleCollider collider, Vector3 worldVertex)
    {
        float x = Math.Min(Vector3.Angle(collider.transform.right, worldVertex - collider.transform.position), Vector3.Angle(-collider.transform.right, worldVertex - collider.transform.position));
        float y = Math.Min(Vector3.Angle(collider.transform.up, worldVertex - collider.transform.position), Vector3.Angle(-collider.transform.up, worldVertex - collider.transform.position));
        float z = Math.Min(Vector3.Angle(collider.transform.forward, worldVertex - collider.transform.position), Vector3.Angle(-collider.transform.forward, worldVertex - collider.transform.position));
        if (x <= Math.Min(y, z))
        {
            return 0;
        }
        else if (y <= Math.Min(x, z))
        {
            return 1;
        }
        else if (z <= Math.Min(x, y))
        {
            return 2;
        }
        else
        {
            return 0;
        }
    }

    internal static void UpdateRadius(this CapsuleCollider collider, Vector3 worldVertex)
    {
        Debug.Log($"Using radius {collider.transform.position} -> {worldVertex} with distance {(worldVertex - collider.transform.position).magnitude}.", collider.gameObject);
        Debug.DrawRay(collider.transform.position, worldVertex - collider.transform.position, Color.magenta, 60);
        collider.radius = collider.transform.InverseTransformPoint(worldVertex).magnitude;
    }
    internal static void UpdateHeight(this CapsuleCollider collider, Vector3 worldVertex)
    {
        Debug.Log($"Using height {collider.transform.position} -> {worldVertex} with distance {(worldVertex - collider.transform.position).magnitude}.", collider.gameObject);
        Debug.DrawRay(collider.transform.position, worldVertex - collider.transform.position, Color.cyan, 60);
        collider.height = collider.transform.InverseTransformPoint(worldVertex).magnitude;
    }
    internal static void ReflectionRestoreToBindPose(this GameObject gameObject)
    {
        if (gameObject == null)
            return;
        Type type = Type.GetType("UnityEditor.AvatarSetupTool, UnityEditor");
        if (type != null)
        {
            MethodInfo info = type.GetMethod("SampleBindPose", BindingFlags.Static | BindingFlags.Public);
            if (info != null)
            {
                info.Invoke(null, new object[] { gameObject });
            }
        }
    }
}

public class AutomaticColliderFitting : ScriptableWizard
{
    [field: SerializeField]
    public SkinnedMeshRenderer SkinnedMeshRenderer { get; set; }

    [field: SerializeField]
    public Cloth[] Clothes { get; set; }

    [field: SerializeField]
    public float ScaleFactor { get; set; } = 1.0f;

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

        this.SkinnedMeshRenderer.gameObject.ReflectionRestoreToBindPose();

        var meshCollider = this.SkinnedMeshRenderer.transform.root.gameObject.AddComponent<MeshCollider>();
        try
        {
            Physics.queriesHitBackfaces = true;

            Mesh colliderMesh = new Mesh();
            this.SkinnedMeshRenderer.BakeMesh(colliderMesh);
            meshCollider.sharedMesh = null;
            meshCollider.sharedMesh = colliderMesh;

            foreach (var bone in this.SkinnedMeshRenderer.bones)
            {
                if (bone == null) continue;
                var collider = Undo.AddComponent<CapsuleCollider>(bone.gameObject);

                if (UpdateCollider(meshCollider, collider))
                {
                    bool overlapped = Physics.ComputePenetration(
                        collider, collider.transform.position, collider.transform.rotation,
                        meshCollider, meshCollider.transform.position, meshCollider.transform.rotation,
                        out Vector3 _, out float _
                    );

                    if (overlapped)
                    {
                        Debug.Log($"Overlapping {collider.radius} {collider.height}.", collider.gameObject);
                        Selection.objects = default;
                        Selection.activeObject = collider;
                        SceneView.lastActiveSceneView.LookAtDirect(collider.transform.position, SceneView.lastActiveSceneView.rotation);
                        SceneView.RepaintAll();
                        yield return null;

                        if (EditorUtility.DisplayDialog("CapsuleCollider overlaps MeshCollider.", "Action for CapsuleCollider?", "Add", "Remove"))
                        {
                            collider.radius *= this.ScaleFactor;
                            collider.height *= this.ScaleFactor;
                            colliders.Add(collider);
                            continue;
                        }
                        else
                        {
                            DestroyImmediate(collider);
                            continue;
                        }
                    }
                }
                else
                {
                    DestroyImmediate(collider);
                    continue;
                }
            }
        }
        finally
        {
            DestroyImmediate(meshCollider);
            // Restore setting
            Physics.queriesHitBackfaces = queriesHitBackfaces;
        }

        if (this.Clothes != null)
        {
            foreach (var cloth in this.Clothes)
            {
                cloth.capsuleColliders = colliders.ToArray();
            }
        }
    }

    private static bool UpdateCollider(MeshCollider meshCollider, CapsuleCollider collider)
    {
        List<RaycastHit> raycastHits = GetRayCastHits(meshCollider, collider);
        if (raycastHits.Any())
        {
            var firstDirectionClosest = raycastHits.OrderBy(x => x.distance).FirstOrDefault();
            collider.UpdateRadius(firstDirectionClosest.point);
            int firstIgnoreDirection = collider.GetDirection(firstDirectionClosest.point);
            raycastHits.RemoveAll(x => collider.GetDirection(x.point) == firstIgnoreDirection);
            if (raycastHits.Any())
            {
                var secondDirectionClosest = raycastHits.OrderBy(x => x.distance).FirstOrDefault();
                int secondIgnoreDirection = collider.GetDirection(secondDirectionClosest.point);
                raycastHits.RemoveAll(x => collider.GetDirection(x.point) == secondIgnoreDirection);
                if (raycastHits.Any())
                {
                    var thirdDirectionClosest = raycastHits.OrderBy(x => x.distance).FirstOrDefault();
                    collider.UpdateHeight(thirdDirectionClosest.point);
                    collider.direction = collider.GetDirection(thirdDirectionClosest.point);
                    return true;
                }
            }
        }
        return false;
    }

    private static List<RaycastHit> GetRayCastHits(MeshCollider meshCollider, CapsuleCollider collider)
    {
        List<RaycastHit> raycastHits = new List<RaycastHit>();
        foreach (var direction in new[] { collider.transform.up, collider.transform.right, collider.transform.forward, -collider.transform.up, -collider.transform.right, -collider.transform.forward })
        {
            if (meshCollider.Raycast(new Ray(collider.transform.position, collider.transform.TransformDirection(direction)), out RaycastHit hit, meshCollider.bounds.size.magnitude))
            {
                raycastHits.Add(hit);
            }
        }

        return raycastHits;
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
