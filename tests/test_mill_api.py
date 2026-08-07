# ============================================================
# NX CAM Milling Tool API Debugger
#
# Run in NX (Ctrl+U) to test which type/subtype combinations
# work on your NX version for creating milling tools.
#
# The script tries each candidate and reports success/failure
# in the NX Listing Window.
# ============================================================

import NXOpen
import NXOpen.CAM

CANDIDATES = [
    ("mill_planar", "MILL"),
    ("mill_planar", "BALL_MILL"),
    ("mill_planar", "MILLING_TOOL"),
    ("mill_planar", "CHAMFER_MILL"),
]


def safe_find(camGroupCol, name):
    try:
        return camGroupCol.FindObject(name)
    except NXOpen.NXException:
        return None


def try_create_mill_tool(theSession, type_name, subtype_name):
    workPart = theSession.Parts.Work
    camSetup = workPart.CAMSetup
    camGroupCol = camSetup.CAMGroupCollection
    machineRoot = camGroupCol.FindObject("GENERIC_MACHINE")

    test_name = "TEST_MILL_" + subtype_name

    listing = theSession.ListingWindow
    listing.Open()

    listing.WriteLine("=" * 60)
    listing.WriteLine("Test: type=" + type_name + ", subtype=" + subtype_name)
    listing.WriteLine("=" * 60)

    existing = safe_find(camGroupCol, test_name)
    if existing is not None:
        listing.WriteLine("  -> Test tool already exists, skipping")
        listing.Close()
        return True

    try:
        tool = camGroupCol.CreateTool(
            machineRoot, type_name, subtype_name,
            NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue,
            test_name
        )
        listing.WriteLine("  [OK] Tool object created")

        builder = camGroupCol.CreateMillToolBuilder(tool)
        builder.TlDiameterBuilder.Value = 10.0
        builder.TlFluteLnBuilder.Value = 20
        builder.TlNumFlutesBuilder.Value = 2
        builder.Commit()
        builder.Destroy()
        listing.WriteLine("  [OK] Builder committed (dia=10.0)")
        listing.WriteLine("")
        listing.WriteLine("  >>>> SUCCESS! Use this combination: <<<<")
        listing.WriteLine('  type    = "' + type_name + '"')
        listing.WriteLine('  subtype = "' + subtype_name + '"')
        listing.Close()
        return True

    except Exception as e:
        listing.WriteLine("  [FAIL] " + str(e))
        listing.Close()
        return False


def main():
    theSession = NXOpen.Session.GetSession()

    print("NX CAM Mill Tool API Debugger")
    print("Testing type/subtype combinations...")
    for t, s in CANDIDATES:
        print("  - " + t + " / " + s)

    successes = 0
    for type_name, subtype_name in CANDIDATES:
        ok = try_create_mill_tool(theSession, type_name, subtype_name)
        if ok:
            successes += 1
        else:
            print("  FAILED: " + type_name + " / " + subtype_name)

    print("")
    print("Result: " + str(successes) + "/" + str(len(CANDIDATES)) + " succeeded")
    if successes == 0:
        print("All failed! Record a Journal sequence and inspect the generated code.")


if __name__ == "__main__":
    main()
